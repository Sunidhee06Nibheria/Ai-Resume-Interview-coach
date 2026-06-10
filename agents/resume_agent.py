from __future__ import annotations

import re

from agents.base import BaseAgent
from analytics.keywords import extract_keywords, split_bullets
from analytics.scoring import has_quantified_impact, score_resume
from models import ResumeAnalysis, ResumeSections


class ResumeAgent(BaseAgent):
    name = "resume-agent"

    def analyze(self, resume_text: str) -> ResumeAnalysis:
        sections = ResumeSections(
            skills=extract_keywords(resume_text),
            projects=self._extract_section_lines(resume_text, ["project", "projects"]),
            experience=self._extract_section_lines(resume_text, ["experience", "work"]),
            education=self._extract_section_lines(resume_text, ["education", "degree"]),
            certifications=self._extract_section_lines(resume_text, ["certification", "certificate"]),
        )
        scores = score_resume(resume_text)
        bullets = split_bullets(resume_text)
        weak_bullets = [bullet for bullet in bullets if not has_quantified_impact(bullet)][:4]

        strengths = []
        if sections.skills:
            strengths.append(f"Shows practical technical breadth across {len(sections.skills)} detected skills.")
        if scores.project_quality_score >= 60:
            strengths.append("Project section signals implementation depth and measurable work.")
        if scores.leadership_score >= 45:
            strengths.append("Resume contains ownership and leadership language.")
        if not strengths:
            strengths.append("The resume has enough raw material to improve with clearer structure and stronger evidence.")

        risks = []
        if scores.ats_score < 70:
            risks.append("ATS score is limited by missing keywords, sections, or scannable bullet structure.")
        if scores.technical_strength_score < 65:
            risks.append("Technical depth needs more tools, architecture details, or deployed project evidence.")
        if scores.leadership_score < 45:
            risks.append("Leadership and ownership signals are underrepresented.")

        recommendations = [
            "Add a dedicated skills section grouped by languages, frameworks, AI/ML, databases, and cloud.",
            "Convert responsibilities into impact bullets using action verb, technical method, and measurable result.",
            "Include deployment, users, latency, accuracy, cost, or automation metrics wherever truthful.",
        ]

        improved = [self._rewrite_bullet(bullet) for bullet in weak_bullets]

        return ResumeAnalysis(
            sections=sections,
            scores=scores,
            strengths=strengths,
            risks=risks,
            recommendations=recommendations,
            improved_bullets=improved,
        )

    def _extract_section_lines(self, text: str, labels: list[str]) -> list[str]:
        lines = [line.strip(" -•\t") for line in text.splitlines() if line.strip()]
        matched = [line for line in lines if any(label in line.lower() for label in labels)]
        return matched[:8]

    def _rewrite_bullet(self, bullet: str) -> str:
        cleaned = re.sub(r"\s+", " ", bullet).strip(". ")
        return f"Engineered {cleaned} by clarifying scope, implementation approach, and measurable impact."

