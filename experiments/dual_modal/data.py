from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch import Tensor
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset

from experiments.dual_modal.tokenizer import OCRTokenizer


class OCRImageDataset(Dataset):
    def __init__(
        self,
        image_dir: Path,
        label_file: Path,
        tokenizer: OCRTokenizer,
        img_height: int = 32,
        img_width: int = 320,
        max_samples: int = 0,
    ) -> None:
        self.image_dir = image_dir
        self.tokenizer = tokenizer
        self.img_height = img_height
        self.img_width = img_width
        self.rows = []

        with label_file.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                filename = (row.get("filename") or "").strip()
                text = (row.get("text") or row.get("gt_text") or "").strip()
                if not filename or not text:
                    continue
                image_path = image_dir / filename
                if not image_path.exists():
                    continue
                self.rows.append({"filename": filename, "text": text})
                if max_samples and len(self.rows) >= max_samples:
                    break

    def __len__(self) -> int:
        return len(self.rows)

    def _load_image(self, image_path: Path) -> Tensor:
        image = Image.open(image_path).convert("L")
        ratio = min(self.img_width / image.width, self.img_height / image.height)
        resized = image.resize(
            (max(1, int(image.width * ratio)), max(1, int(image.height * ratio))),
            Image.BILINEAR,
        )
        canvas = Image.new("L", (self.img_width, self.img_height), color=255)
        offset_x = (self.img_width - resized.width) // 2
        offset_y = (self.img_height - resized.height) // 2
        canvas.paste(resized, (offset_x, offset_y))
        array = np.asarray(canvas, dtype=np.float32) / 255.0
        array = 1.0 - array
        return torch.from_numpy(array).unsqueeze(0)

    def __getitem__(self, idx: int) -> dict[str, Tensor | str]:
        row = self.rows[idx]
        label_ids = self.tokenizer.encode(row["text"])
        return {
            "filename": row["filename"],
            "text": row["text"],
            "image": self._load_image(self.image_dir / row["filename"]),
            "label_ids": torch.tensor(label_ids, dtype=torch.long),
        }


def collate_batch(batch: list[dict[str, Tensor | str]]) -> dict[str, Tensor | list[str]]:
    images = torch.stack([item["image"] for item in batch])  # type: ignore[index]
    filenames = [str(item["filename"]) for item in batch]
    texts = [str(item["text"]) for item in batch]
    label_ids = [item["label_ids"] for item in batch]  # type: ignore[index]
    target_lengths = torch.tensor([len(ids) for ids in label_ids], dtype=torch.long)
    flat_targets = torch.cat(label_ids) if label_ids else torch.empty(0, dtype=torch.long)
    semantic_ids = pad_sequence(label_ids, batch_first=True, padding_value=0)
    return {
        "images": images,
        "filenames": filenames,
        "texts": texts,
        "semantic_ids": semantic_ids,
        "targets": flat_targets,
        "target_lengths": target_lengths,
    }

