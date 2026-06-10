from __future__ import annotations

import tempfile
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from agents.interview_agent import InterviewAgent
from analytics.scoring import score_job_match
from parsers.document_parser import clean_text, parse_docx, parse_pdf
from reports.markdown import resume_report_to_markdown
from workflows.career_workflow import run_resume_workflow


def main() -> None:
    st.set_page_config(page_title="AI Resume & Interview Coach", page_icon="AI", layout="wide")
    inject_css()
    st.sidebar.title("Career Copilot")
    page = st.sidebar.radio(
        "Workspace",
        [
            "Home",
            "Resume Analysis",
            "ATS Checker",
            "Job Match Analyzer",
            "Career Coach",
            "Interview Simulator",
            "Learning Roadmap",
            "Profile Analytics",
            "Settings",
        ],
    )

    if page == "Home":
        home()
    elif page == "Resume Analysis":
        resume_analysis()
    elif page == "ATS Checker":
        ats_checker()
    elif page == "Job Match Analyzer":
        job_match()
    elif page == "Career Coach":
        career_coach()
    elif page == "Interview Simulator":
        interview_simulator()
    elif page == "Learning Roadmap":
        learning_roadmap()
    elif page == "Profile Analytics":
        profile_analytics()
    else:
        settings()


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; }
        div[data-testid="stMetric"] { border: 1px solid #e6e8ec; border-radius: 8px; padding: 12px; background: #ffffff; }
        .stButton button { border-radius: 8px; font-weight: 600; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def home() -> None:
    st.title("AI Resume & Interview Coach")
    st.caption("Agentic resume intelligence, ATS analysis, job matching, career planning, and interview practice.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resume Score", "82", "+12")
    col2.metric("ATS Score", "76", "+9")
    col3.metric("Interview Readiness", "71", "+15")
    col4.metric("Skill Coverage", "68%", "+18%")
    st.subheader("System Capabilities")
    st.write(
        "Upload a resume, compare it with a job description, generate a skill roadmap, and practice interview answers with structured feedback."
    )


def resume_analysis() -> None:
    st.title("Resume Analysis")
    resume_text = get_resume_text()
    if st.button("Run Full Analysis", type="primary") and resume_text:
        report = run_resume_workflow(resume_text)
        render_report(report)
        st.download_button("Download Markdown Report", resume_report_to_markdown(report), file_name="resume_report.md")


def ats_checker() -> None:
    st.title("ATS Checker")
    resume_text = get_resume_text("ats")
    jd = st.text_area("Optional job description", height=180)
    if st.button("Analyze ATS Fit", type="primary") and resume_text:
        report = run_resume_workflow(resume_text, jd)
        ats = report["ats_report"]
        st.subheader("ATS Optimization Report")
        st.write("Missing keywords:", ", ".join(ats["missing_keywords"]) or "No critical gaps detected")
        st.write("Formatting issues")
        st.write(ats["formatting_issues"])
        st.write("Suggestions")
        st.write(ats["suggestions"])


def job_match() -> None:
    st.title("Job Match Analyzer")
    resume_text = get_resume_text("match")
    jd = st.text_area("Paste job description", height=240)
    if st.button("Calculate Match", type="primary") and resume_text and jd:
        report = score_job_match(resume_text, jd)
        st.metric("Match Percentage", f"{report.match_percentage}%")
        st.progress(report.match_percentage / 100)
        st.write("Missing skills", report.missing_skills)
        st.write("Keyword gap", report.keyword_gap)
        st.write("Recommendations", report.recommendation_report)


def career_coach() -> None:
    st.title("Career Coach")
    resume_text = get_resume_text("coach")
    role = st.selectbox("Desired role", ["AI Engineer", "Machine Learning Engineer", "Data Scientist", "Software Engineer"])
    if st.button("Generate Career Plan", type="primary") and resume_text:
        report = run_resume_workflow(resume_text, desired_role=role)
        st.write(report["career_plan"])


def interview_simulator() -> None:
    st.title("Interview Simulator")
    role = st.text_input("Role", "AI Engineer")
    interview_type = st.selectbox("Interview type", ["technical", "behavioral", "hr", "ai/ml", "product"])
    agent = InterviewAgent()
    questions = agent.generate_questions(role, interview_type)
    selected = st.selectbox("Question", questions.questions)
    answer = st.text_area("Your answer", height=220)
    if st.button("Evaluate Answer", type="primary") and answer:
        feedback = agent.evaluate_answer(selected, answer, role)
        st.metric("Feedback Score", f"{feedback.feedback_score}/100")
        st.write(feedback.model_dump())


def learning_roadmap() -> None:
    st.title("Learning Roadmap")
    resume_text = get_resume_text("roadmap")
    role = st.selectbox("Target role", ["AI Engineer", "Machine Learning Engineer", "Data Scientist", "Software Engineer"], key="roadmap_role")
    if st.button("Build Roadmap", type="primary") and resume_text:
        report = run_resume_workflow(resume_text, desired_role=role)
        st.write(report["skill_gap_report"]["weekly_learning_roadmap"])


def profile_analytics() -> None:
    st.title("Profile Analytics")
    sample = {"ATS": 76, "Technical": 84, "Leadership": 58, "Projects": 80, "Employability": 77}
    fig = go.Figure(data=[go.Bar(x=list(sample.keys()), y=list(sample.values()), marker_color="#2563eb")])
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def settings() -> None:
    st.title("Settings")
    st.text_input("LLM provider", "local")
    st.text_input("Embedding model", "sentence-transformers/all-MiniLM-L6-v2")
    st.info("The app runs locally without API keys. Add Gemini or OpenAI-compatible keys in .env for hosted model calls.")


def get_resume_text(key_suffix: str = "resume") -> str:
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"], key=f"upload_{key_suffix}")
    fallback = st.text_area("Or paste resume text", height=220, key=f"text_{key_suffix}")
    if uploaded:
        content = uploaded.read()
        suffix = Path(uploaded.name).suffix.lower()
        if suffix == ".pdf":
            return clean_text(parse_pdf(content))
        if suffix == ".docx":
            return clean_text(parse_docx(content))
        return clean_text(content.decode("utf-8", errors="ignore"))
    return fallback


def render_report(report: dict) -> None:
    st.subheader(report["executive_summary"])
    scores = report["resume_analysis"]["scores"]
    cols = st.columns(6)
    for col, (name, value) in zip(cols, scores.items()):
        col.metric(name.replace("_", " ").title(), f"{value}/100")
    st.write("Strengths", report["resume_analysis"]["strengths"])
    st.write("Risks", report["resume_analysis"]["risks"])
    st.write("Recommendations", report["resume_analysis"]["recommendations"])
    st.write("Improved bullets", report["resume_analysis"]["improved_bullets"])

