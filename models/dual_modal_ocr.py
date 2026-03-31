from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn


@dataclass
class SingleModalOutput:
    logits: Tensor


@dataclass
class DualModalOutput:
    visual_logits: Tensor
    fused_logits: Tensor
    semantic_ids: Tensor


class VisualEncoder(nn.Module):
    def __init__(self, hidden_size: int) -> None:
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1), (2, 1)),
            nn.Conv2d(128, hidden_size, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1), (2, 1)),
        )
        self.sequence_encoder = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size // 2,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
        )

    def forward(self, images: Tensor) -> Tensor:
        features = self.backbone(images)
        features = features.mean(dim=2)
        sequence = features.permute(0, 2, 1)
        encoded, _ = self.sequence_encoder(sequence)
        return encoded


class SemanticEncoder(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, hidden_size: int) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.sequence_encoder = nn.GRU(
            input_size=embed_dim,
            hidden_size=hidden_size // 2,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
        )

    def forward(self, semantic_ids: Tensor) -> Tensor:
        embedded = self.embedding(semantic_ids)
        encoded, _ = self.sequence_encoder(embedded)
        mask = (semantic_ids != 0).unsqueeze(-1)
        summed = (encoded * mask).sum(dim=1)
        lengths = mask.sum(dim=1).clamp(min=1)
        return summed / lengths


class GatedFusion(nn.Module):
    def __init__(self, hidden_size: int) -> None:
        super().__init__()
        self.visual_proj = nn.Linear(hidden_size, hidden_size)
        self.semantic_proj = nn.Linear(hidden_size, hidden_size)
        self.output_proj = nn.Linear(hidden_size, hidden_size)

    def forward(self, visual_sequence: Tensor, semantic_summary: Tensor) -> Tensor:
        semantic_expand = semantic_summary.unsqueeze(1).expand(-1, visual_sequence.size(1), -1)
        gate = torch.sigmoid(self.visual_proj(visual_sequence) + self.semantic_proj(semantic_expand))
        fused = gate * visual_sequence + (1.0 - gate) * semantic_expand
        return self.output_proj(fused)


class SingleModalOCR(nn.Module):
    def __init__(self, vocab_size: int, hidden_size: int = 256) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.visual_encoder = VisualEncoder(hidden_size=hidden_size)
        self.classifier = nn.Linear(hidden_size, vocab_size)

    def forward(self, images: Tensor) -> SingleModalOutput:
        visual_sequence = self.visual_encoder(images)
        logits = self.classifier(visual_sequence)
        return SingleModalOutput(logits=logits)


class DualModalOCR(nn.Module):
    def __init__(self, vocab_size: int, hidden_size: int = 256, embed_dim: int = 128) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.embed_dim = embed_dim

        self.visual_encoder = VisualEncoder(hidden_size=hidden_size)
        self.semantic_encoder = SemanticEncoder(
            vocab_size=vocab_size,
            embed_dim=embed_dim,
            hidden_size=hidden_size,
        )
        self.fusion = GatedFusion(hidden_size=hidden_size)
        self.visual_classifier = nn.Linear(hidden_size, vocab_size)
        self.fused_classifier = nn.Linear(hidden_size, vocab_size)

    def _build_semantic_ids_from_logits(self, logits: Tensor) -> Tensor:
        batch_tokens: list[list[int]] = []
        token_ids = logits.argmax(dim=-1).detach().cpu().tolist()
        for seq in token_ids:
            collapsed = []
            prev = -1
            for token in seq:
                if token != 0 and token != prev:
                    collapsed.append(token)
                prev = token
            batch_tokens.append(collapsed or [0])

        max_len = max(len(seq) for seq in batch_tokens)
        semantic_ids = torch.zeros((len(batch_tokens), max_len), dtype=torch.long, device=logits.device)
        for idx, seq in enumerate(batch_tokens):
            if seq and seq[0] != 0:
                semantic_ids[idx, : len(seq)] = torch.tensor(seq, dtype=torch.long, device=logits.device)
        return semantic_ids

    def forward(self, images: Tensor, semantic_ids: Tensor | None = None) -> DualModalOutput:
        visual_sequence = self.visual_encoder(images)
        visual_logits = self.visual_classifier(visual_sequence)

        if semantic_ids is None:
            semantic_ids = self._build_semantic_ids_from_logits(visual_logits)

        semantic_summary = self.semantic_encoder(semantic_ids)
        fused_sequence = self.fusion(visual_sequence, semantic_summary)
        fused_logits = self.fused_classifier(fused_sequence)

        return DualModalOutput(
            visual_logits=visual_logits,
            fused_logits=fused_logits,
            semantic_ids=semantic_ids,
        )
