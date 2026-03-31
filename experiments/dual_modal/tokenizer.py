from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OCRTokenizer:
    idx_to_char: list[str]

    @property
    def blank_id(self) -> int:
        return 0

    @property
    def vocab_size(self) -> int:
        return len(self.idx_to_char) + 1

    def encode(self, text: str) -> list[int]:
        mapping = {ch: idx for idx, ch in enumerate(self.idx_to_char, start=1)}
        return [mapping[ch] for ch in text if ch in mapping]

    def decode(self, token_ids: list[int]) -> str:
        chars = []
        for token_id in token_ids:
            if token_id <= 0:
                continue
            if token_id - 1 < len(self.idx_to_char):
                chars.append(self.idx_to_char[token_id - 1])
        return "".join(chars)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"idx_to_char": self.idx_to_char}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "OCRTokenizer":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(idx_to_char=payload["idx_to_char"])

    @classmethod
    def build_from_label_files(cls, label_files: list[Path]) -> "OCRTokenizer":
        charset = set()
        for label_file in label_files:
            if not label_file.exists():
                continue
            with label_file.open("r", encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    charset.update((row.get("text") or "").strip())
        return cls(idx_to_char=sorted(charset))

