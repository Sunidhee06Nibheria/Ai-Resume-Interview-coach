from fastapi import APIRouter, File, Form, UploadFile

from analytics.scoring import score_job_match
from agents.interview_agent import InterviewAgent
from database.repository import save_resume_analysis
from parsers.document_parser import parse_upload
from workflows.career_workflow import run_resume_workflow

router = APIRouter()


@router.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)) -> dict:
    parsed = await parse_upload(file)
    report = run_resume_workflow(parsed.text)
    save_resume_analysis(filename=file.filename or "resume", raw_text=parsed.text, report=report)
    return report


@router.post("/match-job")
async def match_job(file: UploadFile = File(...), job_description: str = Form(...)) -> dict:
    parsed = await parse_upload(file)
    return score_job_match(parsed.text, job_description).model_dump()


@router.post("/interview/questions")
def interview_questions(role: str = Form(...), interview_type: str = Form("technical")) -> dict:
    return InterviewAgent().generate_questions(role=role, interview_type=interview_type).model_dump()


@router.post("/interview/feedback")
def interview_feedback(question: str = Form(...), answer: str = Form(...), role: str = Form("AI Engineer")) -> dict:
    return InterviewAgent().evaluate_answer(question=question, answer=answer, role=role).model_dump()

