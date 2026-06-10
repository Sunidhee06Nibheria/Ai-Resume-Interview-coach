from __future__ import annotations

import hashlib
import math


class EmbeddingProvider:
    def embed(self, texts: list[str]) -> list[list[float]]:
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            return model.encode(texts, normalize_embeddings=True).tolist()
        except Exception:
            return [self._hash_embedding(text) for text in texts]

    def _hash_embedding(self, text: str, dimensions: int = 64) -> list[float]:
        vector = [0.0] * dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

