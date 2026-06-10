from __future__ import annotations

from agents.base import BaseAgent
from analytics.keywords import CORE_SKILLS, extract_keywords, split_bullets


class ATSAgent(BaseAgent):
    name = "ats-agent"

    def optimize(self, resume_text: str, job_description: str = "") -> dict:
        target_terms = set(extract_keywords(job_description)) if job_description else CORE_SKILLS
        present = set(extract_keywords(resume_text, target_terms))
        missing = sorted(target_terms - present)[:12]
        weak_bullets = [bullet for bullet in split_bullets(resume_text) if len(bullet.split()) < 14][:6]
        context = self.retrieve_context("ATS resume keyword achievements bullet points")
        return {
            "missing_keywords": missing,
            "weak_bullets": weak_bullets,
            "formatting_issues": self._formatting_issues(resume_text),
            "suggestions": [
                "Use standard section headers: Summary, Skills, Experience, Projects, Education, Certifications.",
                "Place exact role keywords naturally in project and experience bullets.",
                "Avoid tables, text boxes, excessive icons, and image-only resumes for ATS compatibility.",
                *context[:2],
            ],
            "action_verbs": ["Built", "Designed", "Automated", "Optimized", "Deployed", "Led", "Reduced", "Improved"],
        }

    def _formatting_issues(self, resume_text: str) -> list[str]:
        issues = []
        if len(resume_text) < 900:
            issues.append("Resume appears short; add richer project and impact detail.")
        if "skills" not in resume_text.lower():
            issues.append("Missing explicit Skills section.")
        if "@" not in resume_text:
            issues.append("Contact email was not detected.")
        return issues or ["No major formatting risks detected from plain text extraction."]

