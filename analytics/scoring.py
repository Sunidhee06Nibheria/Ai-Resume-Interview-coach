from __future__ import annotations

import re

from analytics.keywords import ACTION_VERBS, CORE_SKILLS, extract_keywords, normalize_text, split_bullets
from models import JobMatchReport, ScoreBreakdown


def clamp(value: float) -> int:
    return max(0, min(100, round(value)))


def has_quantified_impact(text: str) -> bool:
    return bool(re.search(r"(\d+%|\$\d+|\b\d+x\b|\b\d+\+?\b)", text.lower()))


def score_resume(text: str) -> ScoreBreakdown:
    normalized = normalize_text(text)
    skills = extract_keywords(text)
    bullets = split_bullets(text)
    quantified = sum(1 for bullet in bullets if has_quantified_impact(bullet))
    action_verb_hits = sum(1 for verb in ACTION_VERBS if verb in normalized)

    section_hits = sum(
        1
        for section in ["experience", "projects", "education", "skills", "certifications"]
        if section in normalized
    )
    ats = clamp(12 + (len(skills) / 14) * 48 + (section_hits / 5) * 30 + min(len(bullets), 10) * 3)
    technical = clamp(10 + (len(skills) / 16) * 78 + (1 if "github" in normalized else 0) * 10 + (1 if "api" in normalized else 0) * 15)
    leadership = clamp(action_verb_hits * 7 + normalized.count("led") * 12 + normalized.count("mentor") * 10)
    project_quality = clamp(10 + normalized.count("project") * 10 + quantified * 10 + ("deployed" in normalized) * 15)
    employability = clamp(ats * 0.35 + technical * 0.3 + leadership * 0.15 + project_quality * 0.2)
    resume = clamp(ats * 0.3 + technical * 0.25 + leadership * 0.15 + project_quality * 0.15 + employability * 0.15)

    return ScoreBreakdown(
        resume_score=resume,
        ats_score=ats,
        technical_strength_score=technical,
        leadership_score=leadership,
        project_quality_score=project_quality,
        employability_score=employability,
    )


def score_job_match(resume_text: str, job_description: str) -> JobMatchReport:
    resume_skills = set(extract_keywords(resume_text))
    jd_skills = set(extract_keywords(job_description))
    jd_words = {
        word
        for word in re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", normalize_text(job_description))
        if len(word) > 3
    }
    resume_words = set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", normalize_text(resume_text)))
    keyword_gap = sorted((jd_words - resume_words) & (CORE_SKILLS | jd_skills))[:12]
    missing_skills = sorted(jd_skills - resume_skills)
    denominator = max(len(jd_skills), 1)
    match = clamp((len(resume_skills & jd_skills) / denominator) * 78 + (1 - min(len(keyword_gap), 10) / 10) * 22)
    readiness = clamp(match * 0.7 + score_resume(resume_text).technical_strength_score * 0.3)

    recommendations = [
        "Mirror high-priority job-description keywords in the skills and project sections.",
        "Rewrite bullets to include measurable business or technical impact.",
        "Add one role-aligned project that demonstrates the missing technical skill set.",
    ]
    if missing_skills:
        recommendations.insert(0, f"Prioritize these skills first: {', '.join(missing_skills[:5])}.")

    return JobMatchReport(
        match_percentage=match,
        missing_skills=missing_skills,
        keyword_gap=keyword_gap,
        recommendation_report=recommendations,
        interview_readiness_score=readiness,
    )
