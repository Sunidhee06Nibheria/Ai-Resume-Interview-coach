from __future__ import annotations

import re


CORE_SKILLS = {
    "python",
    "sql",
    "fastapi",
    "streamlit",
    "docker",
    "aws",
    "gcp",
    "azure",
    "machine learning",
    "deep learning",
    "nlp",
    "rag",
    "langchain",
    "langgraph",
    "vector search",
    "faiss",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "mlops",
    "api",
    "sqlite",
    "postgresql",
}

ACTION_VERBS = {
    "built",
    "designed",
    "implemented",
    "optimized",
    "deployed",
    "automated",
    "led",
    "owned",
    "improved",
    "reduced",
    "increased",
    "launched",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_keywords(text: str, vocabulary: set[str] | None = None) -> list[str]:
    normalized = normalize_text(text)
    terms = vocabulary or CORE_SKILLS
    return sorted(term for term in terms if term in normalized)


def split_bullets(text: str) -> list[str]:
    lines = [line.strip(" -•\t") for line in text.splitlines()]
    bullets = [line for line in lines if len(line.split()) >= 5]
    if bullets:
        return bullets[:20]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [sentence.strip() for sentence in sentences if len(sentence.split()) >= 7][:20]

