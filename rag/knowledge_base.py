from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from embeddings.provider import EmbeddingProvider
from rag.seed_knowledge import SEED_DOCUMENTS


@dataclass(frozen=True)
class Chunk:
    text: str
    score: float = 0.0


class KnowledgeBase:
    def __init__(self, chunks: list[str]) -> None:
        self.chunks = chunks
        self.embedding_provider = EmbeddingProvider()
        self.embeddings = np.array(self.embedding_provider.embed(chunks), dtype=np.float32)

    @classmethod
    def load_default(cls) -> "KnowledgeBase":
        return cls(SEED_DOCUMENTS)

    def search(self, query: str, k: int = 3) -> list[Chunk]:
        query_embedding = np.array(self.embedding_provider.embed([query])[0], dtype=np.float32)
        scores = self.embeddings @ query_embedding
        ranked = scores.argsort()[::-1][:k]
        return [Chunk(text=self.chunks[index], score=float(scores[index])) for index in ranked]

