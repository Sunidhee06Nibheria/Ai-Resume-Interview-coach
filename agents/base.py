from __future__ import annotations

from dataclasses import dataclass

from rag.knowledge_base import KnowledgeBase


@dataclass
class AgentContext:
    resume_text: str
    job_description: str = ""
    desired_role: str = "AI Engineer"


class BaseAgent:
    name = "base-agent"

    def __init__(self, knowledge_base: KnowledgeBase | None = None) -> None:
        self.knowledge_base = knowledge_base or KnowledgeBase.load_default()

    def retrieve_context(self, query: str, k: int = 3) -> list[str]:
        return [chunk.text for chunk in self.knowledge_base.search(query, k=k)]

