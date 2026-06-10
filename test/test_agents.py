from agents.interview_agent import InterviewAgent
from agents.resume_agent import ResumeAgent


def test_resume_agent_generates_analysis() -> None:
    report = ResumeAgent().analyze("Skills: Python FastAPI RAG FAISS\nProjects\nBuilt API used by 100 users.")
    assert report.scores.resume_score >= 0
    assert report.recommendations


def test_interview_agent_feedback() -> None:
    feedback = InterviewAgent().evaluate_answer(
        "How would you design a RAG system?",
        "First I would define retrieval metrics, then build embeddings, evaluate answer quality, and monitor latency.",
    )
    assert feedback.feedback_score >= 35
