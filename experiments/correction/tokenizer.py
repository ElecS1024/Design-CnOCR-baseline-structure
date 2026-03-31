from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CorrectionTokenizer:
    idx_to_char: list[str]

    pad_token: str = "<pad>"
    sos_token: str = "<sos>"
    eos_token: str = "<eos>"
    unk_token: str = "<unk>"

    @property
    def pad_id(self) -> int:
        return 0

    @property
    def sos_id(self) -> int:
        return 1

    @property
    def eos_id(self) -> int:
        return 2

    @property
    def unk_id(self) -> int:
        return 3

    @property
    def vocab_size(self) -> int:
        return len(self.idx_to_char) + 4

    def _mapping(self) -> dict[str, int]:
        return {ch: idx for idx, ch in enumerate(self.idx_to_char, start=4)}

    def encode_source(self, text: str, max_length: int = 0) -> list[int]:
        tokens = [self._mapping().get(ch, self.unk_id) for ch in text]
        if max_length > 0:
            tokens = tokens[:max_length]
        return tokens or [self.pad_id]

    def encode_target(self, text: str, max_length: int = 0) -> list[int]:
        core = [self._mapping().get(ch, self.unk_id) for ch in text]
        if max_length > 0:
            core = core[: max(0, max_length - 2)]
        return [self.sos_id, *core, self.eos_id]

    def decode(self, token_ids: list[int]) -> str:
        chars = []
        for token_id in token_ids:
            if token_id in {self.pad_id, self.sos_id}:
                continue
            if token_id == self.eos_id:
                break
            if token_id >= 4 and token_id - 4 < len(self.idx_to_char):
                chars.append(self.idx_to_char[token_id - 4])
        return "".join(chars)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"idx_to_char": self.idx_to_char}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "CorrectionTokenizer":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(idx_to_char=payload["idx_to_char"])

    @classmethod
    def build_from_csv_files(cls, files: list[Path]) -> "CorrectionTokenizer":
        charset = set()
        for file in files:
            if not file.exists():
                continue
            with file.open("r", encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    baseline_text = (row.get("baseline_text") or row.get("pred_text") or "").strip()
                    target_text = (row.get("target_text") or row.get("gt_text") or "").strip()
                    charset.update(baseline_text)
                    charset.update(target_text)
        return cls(idx_to_char=sorted(charset))
