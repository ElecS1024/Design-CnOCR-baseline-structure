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

from experiments.correction.data import CorrectionDataset, collate_batch
from experiments.correction.tokenizer import CorrectionTokenizer
from models.correction_model import TextCorrectionSeq2Seq


def main() -> int:
    parser = argparse.ArgumentParser(description="Run correction model prediction.")
    root = ROOT
    default_output_dir = root / "outputs" / "correction_model"
    parser.add_argument(
        "--input-csv",
        default=str(root / "outputs" / "correction" / "hard_cases_correction_pairs.csv"),
    )
    parser.add_argument("--checkpoint", default=str(default_output_dir / "checkpoints" / "best.pt"))
    parser.add_argument("--vocab-file", default=str(default_output_dir / "vocab.json"))
    parser.add_argument(
        "--output-file",
        default=str(default_output_dir / "preds" / "hard_cases_preds.csv"),
    )
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--max-samples", type=int, default=0)
    args = parser.parse_args()

    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    config = checkpoint["config"]
    tokenizer = CorrectionTokenizer.load(Path(args.vocab_file))
    model = TextCorrectionSeq2Seq(
        vocab_size=config["vocab_size"],
        embed_dim=config["embed_dim"],
        hidden_size=config["hidden_size"],
        pad_id=tokenizer.pad_id,
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    dataset = CorrectionDataset(
        csv_file=Path(args.input_csv),
        tokenizer=tokenizer,
        max_source_length=config["max_source_length"],
        max_target_length=config["max_target_length"],
        max_samples=args.max_samples,
    )
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        collate_fn=lambda batch: collate_batch(batch, tokenizer.pad_id),
    )

    rows = []
    with torch.no_grad():
        for batch in dataloader:
            source_ids = batch["source_ids"].to(device)
            sequences = model.greedy_decode(
                source_ids,
                sos_id=tokenizer.sos_id,
                eos_id=tokenizer.eos_id,
                max_length=config["max_target_length"],
            )
            pred_texts = [tokenizer.decode(seq) for seq in sequences]
            for filename, gt_text, pred_text, baseline_score in zip(
                batch["filenames"], batch["target_texts"], pred_texts, batch["baseline_scores"]
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

    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["filename", "gt_text", "pred_text", "score", "exact_match"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"correction predictions saved to: {output_file}")
    print(f"pairs processed: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
