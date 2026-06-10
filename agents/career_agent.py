from __future__ import annotations

from agents.base import BaseAgent
from analytics.keywords import extract_keywords


class CareerAgent(BaseAgent):
    name = "career-agent"

    def coach(self, resume_text: str, desired_role: str = "AI Engineer") -> dict:
        skills = set(extract_keywords(resume_text))
        context = self.retrieve_context(f"{desired_role} career roadmap projects certifications")
        project_recs = [
            "RAG resume intelligence platform with evaluation metrics and observability.",
            "Interview simulator with rubric-based scoring and conversation memory.",
            "MLOps pipeline that trains, evaluates, versions, and deploys a model API.",
        ]
        certifications = ["Google Cloud Professional Machine Learning Engineer", "AWS Machine Learning Specialty", "DeepLearning.AI specialization"]
        return {
            "desired_role": desired_role,
            "career_paths": [desired_role, "Machine Learning Engineer", "Applied AI Engineer", "Data Scientist"],
            "suggested_projects": project_recs,
            "suggested_certifications": certifications,
            "internship_strategy": [
                "Target AI platform, search/recommendation, data, and developer tooling teams.",
                "Lead with measurable projects and production engineering depth.",
                "Publish concise case studies for two strongest projects on GitHub and LinkedIn.",
            ],
            "personalized_growth_plan": [
                f"Current detected skills: {', '.join(sorted(skills)) or 'not enough explicit skills detected'}.",
                *context[:3],
            ],
        }

