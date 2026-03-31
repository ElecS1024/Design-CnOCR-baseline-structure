from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import torch
from torch import nn
from torch.optim import AdamW
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.dual_modal.data import OCRImageDataset, collate_batch
from experiments.dual_modal.metrics import compute_metrics
from experiments.dual_modal.tokenizer import OCRTokenizer
from models.dual_modal_ocr import DualModalOCR


def ctc_decode(logits: torch.Tensor, tokenizer: OCRTokenizer) -> tuple[list[str], list[float]]:
    probs = logits.softmax(dim=-1)
    token_ids = probs.argmax(dim=-1)
    texts = []
    scores = []
    for seq_ids, seq_probs in zip(token_ids, probs):
        collapsed = []
        token_scores = []
        prev = -1
        for token, prob in zip(seq_ids.tolist(), seq_probs):
            if token != 0 and token != prev:
                collapsed.append(token)
                token_scores.append(float(prob[token].item()))
            prev = token
        texts.append(tokenizer.decode(collapsed))
        scores.append(sum(token_scores) / len(token_scores) if token_scores else 0.0)
    return texts, scores


def evaluate(
    model: DualModalOCR,
    dataloader: DataLoader,
    tokenizer: OCRTokenizer,
    device: torch.device,
    output_file: Path | None = None,
) -> dict[str, float | int]:
    model.eval()
    rows = []
    with torch.no_grad():
        for batch in dataloader:
            images = batch["images"].to(device)
            outputs = model(images)
            pred_texts, scores = ctc_decode(outputs.fused_logits, tokenizer)
            for filename, gt_text, pred_text, score in zip(
                batch["filenames"], batch["texts"], pred_texts, scores
            ):
                rows.append(
                    {
                        "filename": filename,
                        "gt_text": gt_text,
                        "pred_text": pred_text,
                        "score": f"{score:.6f}",
                        "exact_match": int(gt_text == pred_text),
                    }
                )

    if output_file is not None:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["filename", "gt_text", "pred_text", "score", "exact_match"]
            )
            writer.writeheader()
            writer.writerows(rows)
    return compute_metrics(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a dual-modal OCR experiment model.")
    root = ROOT
    parser.add_argument("--train-dir", default=str(root / "data" / "train"))
    parser.add_argument("--train-labels", default=str(root / "data" / "labels_train.csv"))
    parser.add_argument("--val-dir", default=str(root / "data" / "val"))
    parser.add_argument("--val-labels", default=str(root / "data" / "labels_val.csv"))
    parser.add_argument("--test-labels", default=str(root / "data" / "labels_test.csv"))
    parser.add_argument("--output-dir", default=str(root / "outputs" / "dual_modal"))
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--aux-ctc-weight", type=float, default=0.3)
    parser.add_argument("--hidden-size", type=int, default=256)
    parser.add_argument("--embed-dim", type=int, default=128)
    parser.add_argument("--img-height", type=int, default=32)
    parser.add_argument("--img-width", type=int, default=320)
    parser.add_argument("--max-train-samples", type=int, default=0)
    parser.add_argument("--max-val-samples", type=int, default=0)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--max-steps-per-epoch", type=int, default=0)
    parser.add_argument("--log-interval", type=int, default=100)
    parser.add_argument("--resume-from", default="")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(args.output_dir)
    checkpoint_dir = output_dir / "checkpoints"
    pred_dir = output_dir / "preds"
    eval_dir = output_dir / "eval"
    for path in [checkpoint_dir, pred_dir, eval_dir]:
        path.mkdir(parents=True, exist_ok=True)

    tokenizer = OCRTokenizer.build_from_label_files(
        [Path(args.train_labels), Path(args.val_labels), Path(args.test_labels)]
    )
    vocab_file = output_dir / "vocab.json"
    tokenizer.save(vocab_file)

    train_dataset = OCRImageDataset(
        image_dir=Path(args.train_dir),
        label_file=Path(args.train_labels),
        tokenizer=tokenizer,
        img_height=args.img_height,
        img_width=args.img_width,
        max_samples=args.max_train_samples,
    )
    val_dataset = OCRImageDataset(
        image_dir=Path(args.val_dir),
        label_file=Path(args.val_labels),
        tokenizer=tokenizer,
        img_height=args.img_height,
        img_width=args.img_width,
        max_samples=args.max_val_samples,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=collate_batch,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        collate_fn=collate_batch,
    )

    model = DualModalOCR(
        vocab_size=tokenizer.vocab_size,
        hidden_size=args.hidden_size,
        embed_dim=args.embed_dim,
    ).to(device)
    optimizer = AdamW(model.parameters(), lr=args.learning_rate)
    ctc_loss = nn.CTCLoss(blank=tokenizer.blank_id, zero_infinity=True)

    best_line_accuracy = -1.0
    history = []
    start_epoch = 1

    if args.resume_from:
        resume_path = Path(args.resume_from)
        state = torch.load(resume_path, map_location=device)
        model.load_state_dict(state["model_state_dict"])
        optimizer.load_state_dict(state["optimizer_state_dict"])
        best_line_accuracy = float(state.get("best_line_accuracy", -1.0))
        start_epoch = int(state.get("epoch", 0)) + 1
        print(f"resumed from: {resume_path}, start_epoch={start_epoch}")

    for epoch in range(start_epoch, args.epochs + 1):
        model.train()
        running_loss = 0.0
        steps_ran = 0
        for step, batch in enumerate(train_loader, start=1):
            images = batch["images"].to(device)
            semantic_ids = batch["semantic_ids"].to(device)
            targets = batch["targets"].to(device)
            target_lengths = batch["target_lengths"].to(device)

            outputs = model(images, semantic_ids=semantic_ids)
            visual_log_probs = outputs.visual_logits.log_softmax(dim=-1).permute(1, 0, 2)
            fused_log_probs = outputs.fused_logits.log_softmax(dim=-1).permute(1, 0, 2)
            input_lengths = torch.full(
                (images.size(0),),
                outputs.fused_logits.size(1),
                dtype=torch.long,
                device=device,
            )

            visual_loss = ctc_loss(visual_log_probs, targets, input_lengths, target_lengths)
            fused_loss = ctc_loss(fused_log_probs, targets, input_lengths, target_lengths)
            loss = fused_loss + args.aux_ctc_weight * visual_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item())
            steps_ran = step
            if step % args.log_interval == 0:
                print(
                    f"epoch={epoch} step={step} loss={loss.item():.6f} "
                    f"avg_loss={running_loss / step:.6f}"
                )
            if args.max_steps_per_epoch and step >= args.max_steps_per_epoch:
                break

        val_pred_file = pred_dir / "val_preds.csv"
        val_metrics = evaluate(model, val_loader, tokenizer, device, output_file=val_pred_file)
        avg_train_loss = running_loss / max(steps_ran, 1)
        history.append(
            {
                "epoch": epoch,
                "train_loss": round(avg_train_loss, 6),
                "val_metrics": val_metrics,
            }
        )

        checkpoint = {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch,
            "best_line_accuracy": best_line_accuracy,
            "config": {
                "vocab_size": tokenizer.vocab_size,
                "hidden_size": args.hidden_size,
                "embed_dim": args.embed_dim,
                "img_height": args.img_height,
                "img_width": args.img_width,
            },
        }
        torch.save(checkpoint, checkpoint_dir / "last.pt")
        if float(val_metrics["line_accuracy"]) > best_line_accuracy:
            best_line_accuracy = float(val_metrics["line_accuracy"])
            torch.save(checkpoint, checkpoint_dir / "best.pt")
            (eval_dir / "best_val_metrics.json").write_text(
                json.dumps(val_metrics, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        print(
            f"epoch={epoch} train_loss={avg_train_loss:.6f} "
            f"val_line_acc={float(val_metrics['line_accuracy']):.6f} "
            f"val_char_acc={float(val_metrics['character_accuracy']):.6f}"
        )

    (eval_dir / "train_history.json").write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"training finished, outputs saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
