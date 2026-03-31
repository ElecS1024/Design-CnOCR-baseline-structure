from __future__ import annotations

import csv
from pathlib import Path

import torch
from torch.utils.data import Dataset

from experiments.correction.tokenizer import CorrectionTokenizer


class CorrectionDataset(Dataset):
    def __init__(
        self,
        csv_file: Path,
        tokenizer: CorrectionTokenizer,
        max_source_length: int = 64,
        max_target_length: int = 64,
        max_samples: int = 0,
    ) -> None:
        self.tokenizer = tokenizer
        self.max_source_length = max_source_length
        self.max_target_length = max_target_length
        self.rows: list[dict[str, str]] = []

        with csv_file.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                baseline_text = (row.get("baseline_text") or row.get("pred_text") or "").strip()
                target_text = (row.get("target_text") or row.get("gt_text") or "").strip()
                self.rows.append(
                    {
                        "filename": row["filename"],
                        "source_text": baseline_text,
                        "target_text": target_text,
                        "group": row.get("group", ""),
                        "baseline_score": row.get("baseline_score", row.get("score", "")),
                    }
                )
                if max_samples and len(self.rows) >= max_samples:
                    break

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, object]:
        row = self.rows[index]
        source_ids = self.tokenizer.encode_source(
            row["source_text"], max_length=self.max_source_length
        )
        target_ids = self.tokenizer.encode_target(
            row["target_text"], max_length=self.max_target_length
        )
        return {
            "filename": row["filename"],
            "group": row["group"],
            "source_text": row["source_text"],
            "target_text": row["target_text"],
            "source_ids": torch.tensor(source_ids, dtype=torch.long),
            "target_ids": torch.tensor(target_ids, dtype=torch.long),
            "baseline_score": row["baseline_score"],
        }


def collate_batch(batch: list[dict[str, object]], pad_id: int) -> dict[str, object]:
    batch_size = len(batch)
    max_source_len = max(item["source_ids"].shape[0] for item in batch)
    max_target_len = max(item["target_ids"].shape[0] for item in batch)

    source_ids = torch.full((batch_size, max_source_len), pad_id, dtype=torch.long)
    target_ids = torch.full((batch_size, max_target_len), pad_id, dtype=torch.long)
    source_lengths = torch.zeros(batch_size, dtype=torch.long)
    target_lengths = torch.zeros(batch_size, dtype=torch.long)

    for idx, item in enumerate(batch):
        src = item["source_ids"]
        tgt = item["target_ids"]
        source_ids[idx, : src.shape[0]] = src
        target_ids[idx, : tgt.shape[0]] = tgt
        source_lengths[idx] = src.shape[0]
        target_lengths[idx] = tgt.shape[0]

    return {
        "filenames": [str(item["filename"]) for item in batch],
        "groups": [str(item["group"]) for item in batch],
        "source_texts": [str(item["source_text"]) for item in batch],
        "target_texts": [str(item["target_text"]) for item in batch],
        "baseline_scores": [str(item["baseline_score"]) for item in batch],
        "source_ids": source_ids,
        "target_ids": target_ids,
        "source_lengths": source_lengths,
        "target_lengths": target_lengths,
    }
