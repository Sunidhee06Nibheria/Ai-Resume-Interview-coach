from __future__ import annotations

from agents.base import BaseAgent
from analytics.keywords import extract_keywords


ROLE_SKILLS = {
    "AI Engineer": {"python", "fastapi", "rag", "langchain", "langgraph", "vector search", "faiss", "mlops", "docker"},
    "Machine Learning Engineer": {"python", "scikit-learn", "pytorch", "mlops", "docker", "sql", "aws"},
    "Data Scientist": {"python", "sql", "pandas", "numpy", "machine learning", "scikit-learn"},
    "Software Engineer": {"python", "api", "sql", "docker", "aws", "system design"},
}


class SkillGapAgent(BaseAgent):
    name = "skill-gap-agent"

    def analyze(self, resume_text: str, desired_role: str = "AI Engineer") -> dict:
        current = set(extract_keywords(resume_text))
        target = ROLE_SKILLS.get(desired_role, ROLE_SKILLS["AI Engineer"])
        missing = sorted(target - current)
        return {
            "desired_role": desired_role,
            "current_skills": sorted(current),
            "missing_skills": missing,
            "priority_learning_plan": self._priority_plan(missing),
            "weekly_learning_roadmap": self._weekly_plan(missing),
        }

    def _priority_plan(self, missing: list[str]) -> list[str]:
        return [f"Build one small project or notebook proving {skill}." for skill in missing[:6]] or ["Move from learning to deployment, metrics, and user-facing polish."]

    def _weekly_plan(self, missing: list[str]) -> list[str]:
        focus = missing[:4] or ["resume polish", "mock interviews", "system design", "project case study"]
        return [f"Week {index + 1}: Learn and apply {skill} in a visible portfolio artifact." for index, skill in enumerate(focus)]

