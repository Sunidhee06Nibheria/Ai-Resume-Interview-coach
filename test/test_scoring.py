from analytics.scoring import score_job_match, score_resume


SAMPLE_RESUME = """
Skills: Python, FastAPI, LangChain, RAG, FAISS, SQL, Docker, Streamlit
Projects
- Built a RAG resume analyzer with FastAPI and FAISS that improved retrieval quality by 30%.
- Deployed a Streamlit dashboard used by 50 students for mock interview preparation.
Experience
- Led a team of 3 to automate resume feedback workflows.
Education
B.Tech Computer Science
"""


def test_score_resume_returns_bounded_scores() -> None:
    scores = score_resume(SAMPLE_RESUME)
    assert 0 <= scores.resume_score <= 100
    assert scores.ats_score >= 60
    assert scores.technical_strength_score >= 60


def test_job_match_identifies_missing_skills() -> None:
    report = score_job_match(SAMPLE_RESUME, "Need Python, RAG, LangGraph, Docker, MLOps, FAISS")
    assert report.match_percentage > 40
    assert "langgraph" in report.missing_skills

