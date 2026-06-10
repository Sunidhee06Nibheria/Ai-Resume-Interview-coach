from __future__ import annotations

from analytics.keywords import extract_keywords
from models import InterviewFeedback, InterviewQuestionSet


class InterviewAgent:
    name = "interview-agent"

    def generate_questions(self, role: str, interview_type: str = "technical") -> InterviewQuestionSet:
        base = {
            "technical": [
                f"Design an AI resume analysis system for {role}. How would you structure ingestion, retrieval, scoring, and evaluation?",
                "Explain how you would reduce hallucinations in a RAG-based career coach.",
                "How would you measure the quality of generated resume bullet improvements?",
            ],
            "behavioral": [
                "Tell me about a time you improved a project after receiving critical feedback.",
                "Describe a situation where you had to learn a hard technical topic quickly.",
                "Give an example of ownership you took beyond your assigned work.",
            ],
            "hr": [
                f"Why are you interested in {role} roles?",
                "Walk me through your strongest project.",
                "What kind of team environment helps you do your best work?",
            ],
            "ai/ml": [
                "Compare dense retrieval and keyword retrieval for resume-job matching.",
                "How would you evaluate embedding quality in this product?",
                "What failure modes would you expect from LLM-generated career advice?",
            ],
            "product": [
                "Which user metric would define success for an AI career coach?",
                "How would you prioritize ATS analysis versus mock interview features?",
                "How would you build trust when users rely on AI career recommendations?",
            ],
        }
        questions = base.get(interview_type.lower(), base["technical"])
        return InterviewQuestionSet(
            role=role,
            interview_type=interview_type,
            questions=questions,
            expected_signals=["structured thinking", "tradeoff awareness", "metrics", "ownership", "user empathy"],
            follow_ups=[
                "What would you ship first and why?",
                "How would you monitor this in production?",
                "What would you change if the system had 100,000 users?",
            ],
        )

    def evaluate_answer(self, question: str, answer: str, role: str = "AI Engineer") -> InterviewFeedback:
        words = answer.split()
        skills = extract_keywords(answer)
        structure = sum(marker in answer.lower() for marker in ["first", "second", "because", "tradeoff", "metric", "result"])
        completeness = min(100, len(words) * 2)
        technical = min(100, 12 + len(skills) * 14 + ("architecture" in answer.lower()) * 15 + ("evaluate" in answer.lower()) * 12)
        communication = min(100, 45 + structure * 9)
        confidence = min(100, 35 + min(len(words), 80))
        score = round(completeness * 0.25 + technical * 0.35 + communication * 0.25 + confidence * 0.15)
        return InterviewFeedback(
            feedback_score=score,
            confidence=confidence,
            completeness=completeness,
            technical_depth=technical,
            communication_quality=communication,
            improvement_areas=self._improvement_areas(completeness, technical, communication),
            ideal_answer=f"For a {role} interview, answer with architecture, tradeoffs, evaluation metrics, and a concrete production example tied to the question: {question}",
        )

    def _improvement_areas(self, completeness: int, technical: int, communication: int) -> list[str]:
        areas = []
        if completeness < 70:
            areas.append("Add more complete reasoning with context, action, and result.")
        if technical < 70:
            areas.append("Include deeper technical vocabulary, system design, and evaluation metrics.")
        if communication < 70:
            areas.append("Use a clearer structure with numbered steps and explicit tradeoffs.")
        return areas or ["Strong answer. Improve by adding one quantified result or production lesson."]
