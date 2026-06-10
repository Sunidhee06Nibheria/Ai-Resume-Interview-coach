from __future__ import annotations

from agents.ats_agent import ATSAgent
from agents.career_agent import CareerAgent
from agents.report_agent import ReportAgent
from agents.resume_agent import ResumeAgent
from agents.skill_gap_agent import SkillGapAgent


def run_resume_workflow(resume_text: str, job_description: str = "", desired_role: str = "AI Engineer") -> dict:
    resume_analysis = ResumeAgent().analyze(resume_text).model_dump()
    ats_report = ATSAgent().optimize(resume_text, job_description)
    skill_gap = SkillGapAgent().analyze(resume_text, desired_role)
    career_plan = CareerAgent().coach(resume_text, desired_role)
    return ReportAgent().assemble(
        {
            "resume_analysis": resume_analysis,
            "ats_report": ats_report,
            "skill_gap_report": skill_gap,
            "career_plan": career_plan,
        }
    )

