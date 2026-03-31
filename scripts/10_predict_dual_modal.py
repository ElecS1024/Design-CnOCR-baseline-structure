from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import torch
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.dual_modal.data import OCRImageDataset, collate_batch
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run dual-modal OCR prediction.")
    root = ROOT
    default_output_dir = root / "outputs" / "dual_modal"
    parser.add_argument("--input-dir", default=str(root / "data" / "test"))
    parser.add_argument("--label-file", default=str(root / "data" / "labels_test.csv"))
    parser.add_argument("--checkpoint", default=str(default_output_dir / "checkpoints" / "best.pt"))
    parser.add_argument("--vocab-file", default=str(default_output_dir / "vocab.json"))
    parser.add_argument("--output-file", default=str(default_output_dir / "preds" / "test_preds.csv"))
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--max-samples", type=int, default=0)
    args = parser.parse_args()

    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    config = checkpoint["config"]
    tokenizer = OCRTokenizer.load(Path(args.vocab_file))
    model = DualModalOCR(
        vocab_size=config["vocab_size"],
        hidden_size=config["hidden_size"],
        embed_dim=config["embed_dim"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    dataset = OCRImageDataset(
        image_dir=Path(args.input_dir),
        label_file=Path(args.label_file),
        tokenizer=tokenizer,
        img_height=config["img_height"],
        img_width=config["img_width"],
        max_samples=args.max_samples,
    )
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        collate_fn=collate_batch,
    )

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

    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["filename", "gt_text", "pred_text", "score", "exact_match"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"dual-modal predictions saved to: {output_file}")
    print(f"images processed: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
