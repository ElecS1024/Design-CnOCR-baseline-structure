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

from experiments.correction.data import CorrectionDataset, collate_batch
from experiments.correction.tokenizer import CorrectionTokenizer
from models.correction_model import TextCorrectionSeq2Seq


def evaluate(
    model: TextCorrectionSeq2Seq,
    dataloader: DataLoader,
    tokenizer: CorrectionTokenizer,
    device: torch.device,
    output_file: Path | None = None,
) -> dict[str, float | int]:
    model.eval()
    rows = []
    with torch.no_grad():
        for batch in dataloader:
            source_ids = batch["source_ids"].to(device)
            sequences = model.greedy_decode(
                source_ids,
                sos_id=tokenizer.sos_id,
                eos_id=tokenizer.eos_id,
                max_length=64,
            )
            pred_texts = [tokenizer.decode(seq) for seq in sequences]
            for filename, gt_text, pred_text, baseline_score in zip(
                batch["filenames"],
                batch["target_texts"],
                pred_texts,
                batch["baseline_scores"],
            ):
                rows.append(
                    {
                        "filename": filename,
                        "gt_text": gt_text,
                        "pred_text": pred_text,
                        "score": baseline_score,
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

    total = len(rows)
    exact = sum(int(row["exact_match"]) for row in rows)
    return {
        "total_samples": total,
        "exact_match_samples": exact,
        "line_accuracy": round(exact / total, 6) if total else 0.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a baseline-correction model.")
    root = ROOT
    parser.add_argument(
        "--train-csv",
        default=str(root / "outputs" / "correction" / "full_test_correction_errors_only.csv"),
    )
    parser.add_argument(
        "--val-csv",
        default=str(root / "outputs" / "correction" / "hard_cases_correction_errors_only.csv"),
    )
    parser.add_argument("--output-dir", default=str(root / "outputs" / "correction_model"))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--embed-dim", type=int, default=128)
    parser.add_argument("--hidden-size", type=int, default=256)
    parser.add_argument("--max-source-length", type=int, default=64)
    parser.add_argument("--max-target-length", type=int, default=64)
    parser.add_argument("--max-train-samples", type=int, default=0)
    parser.add_argument("--max-val-samples", type=int, default=0)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--log-interval", type=int, default=50)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(args.output_dir)
    checkpoint_dir = output_dir / "checkpoints"
    pred_dir = output_dir / "preds"
    eval_dir = output_dir / "eval"
    for path in [checkpoint_dir, pred_dir, eval_dir]:
        path.mkdir(parents=True, exist_ok=True)

    tokenizer = CorrectionTokenizer.build_from_csv_files(
        [Path(args.train_csv), Path(args.val_csv)]
    )
    tokenizer.save(output_dir / "vocab.json")

    train_dataset = CorrectionDataset(
        csv_file=Path(args.train_csv),
        tokenizer=tokenizer,
        max_source_length=args.max_source_length,
        max_target_length=args.max_target_length,
        max_samples=args.max_train_samples,
    )
    val_dataset = CorrectionDataset(
        csv_file=Path(args.val_csv),
        tokenizer=tokenizer,
        max_source_length=args.max_source_length,
        max_target_length=args.max_target_length,
        max_samples=args.max_val_samples,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=lambda batch: collate_batch(batch, tokenizer.pad_id),
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        collate_fn=lambda batch: collate_batch(batch, tokenizer.pad_id),
    )

    model = TextCorrectionSeq2Seq(
        vocab_size=tokenizer.vocab_size,
        embed_dim=args.embed_dim,
        hidden_size=args.hidden_size,
        pad_id=tokenizer.pad_id,
    ).to(device)
    optimizer = AdamW(model.parameters(), lr=args.learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_id)

    best_line_acc = -1.0
    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0
        for step, batch in enumerate(train_loader, start=1):
            source_ids = batch["source_ids"].to(device)
            target_ids = batch["target_ids"].to(device)
            decoder_input_ids = target_ids[:, :-1]
            labels = target_ids[:, 1:]

            outputs = model(source_ids, decoder_input_ids)
            loss = criterion(outputs.logits.reshape(-1, tokenizer.vocab_size), labels.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item())
            if step % args.log_interval == 0:
                print(
                    f"epoch={epoch} step={step} loss={loss.item():.6f} "
                    f"avg_loss={running_loss / step:.6f}"
                )

        val_metrics = evaluate(
            model,
            val_loader,
            tokenizer,
            device,
            output_file=pred_dir / "val_preds.csv",
        )
        avg_train_loss = running_loss / max(len(train_loader), 1)
        history.append(
            {
                "epoch": epoch,
                "train_loss": round(avg_train_loss, 6),
                "val_metrics": val_metrics,
            }
        )

        checkpoint = {
            "model_state_dict": model.state_dict(),
            "epoch": epoch,
            "config": {
                "vocab_size": tokenizer.vocab_size,
                "embed_dim": args.embed_dim,
                "hidden_size": args.hidden_size,
                "max_source_length": args.max_source_length,
                "max_target_length": args.max_target_length,
            },
        }
        torch.save(checkpoint, checkpoint_dir / "last.pt")
        if float(val_metrics["line_accuracy"]) > best_line_acc:
            best_line_acc = float(val_metrics["line_accuracy"])
            torch.save(checkpoint, checkpoint_dir / "best.pt")
            (eval_dir / "best_val_metrics.json").write_text(
                json.dumps(val_metrics, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        print(
            f"epoch={epoch} train_loss={avg_train_loss:.6f} "
            f"val_line_acc={float(val_metrics['line_accuracy']):.6f}"
        )

    (eval_dir / "train_history.json").write_text(
        json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"training finished, outputs saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
