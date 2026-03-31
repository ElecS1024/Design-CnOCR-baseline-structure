from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn


@dataclass
class CorrectionOutput:
    logits: Tensor


class TextCorrectionSeq2Seq(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 128,
        hidden_size: int = 256,
        pad_id: int = 0,
    ) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_size = hidden_size
        self.pad_id = pad_id

        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=pad_id)
        self.encoder = nn.GRU(embed_dim, hidden_size, batch_first=True, bidirectional=True)
        self.bridge = nn.Linear(hidden_size * 2, hidden_size)
        self.decoder = nn.GRU(embed_dim, hidden_size, batch_first=True)
        self.output_proj = nn.Linear(hidden_size, vocab_size)

    def encode(self, source_ids: Tensor) -> Tensor:
        embedded = self.embedding(source_ids)
        _, hidden = self.encoder(embedded)
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=-1)
        hidden = torch.tanh(self.bridge(hidden)).unsqueeze(0)
        return hidden

    def forward(self, source_ids: Tensor, decoder_input_ids: Tensor) -> CorrectionOutput:
        hidden = self.encode(source_ids)
        decoder_embedded = self.embedding(decoder_input_ids)
        decoded, _ = self.decoder(decoder_embedded, hidden)
        logits = self.output_proj(decoded)
        return CorrectionOutput(logits=logits)

    def greedy_decode(
        self,
        source_ids: Tensor,
        sos_id: int,
        eos_id: int,
        max_length: int = 64,
    ) -> list[list[int]]:
        hidden = self.encode(source_ids)
        batch_size = source_ids.size(0)
        current = torch.full((batch_size, 1), sos_id, dtype=torch.long, device=source_ids.device)
        sequences = [[] for _ in range(batch_size)]
        finished = [False] * batch_size

        for _ in range(max_length):
            embedded = self.embedding(current)
            decoded, hidden = self.decoder(embedded, hidden)
            logits = self.output_proj(decoded[:, -1:, :])
            next_ids = logits.argmax(dim=-1)
            current = next_ids
            for idx, token in enumerate(next_ids.squeeze(1).tolist()):
                if finished[idx]:
                    continue
                if token == eos_id:
                    finished[idx] = True
                    continue
                sequences[idx].append(token)
            if all(finished):
                break
        return sequences
