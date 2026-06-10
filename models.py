from pydantic import BaseModel, Field


class ResumeSections(BaseModel):
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    resume_score: int
    ats_score: int
    technical_strength_score: int
    leadership_score: int
    project_quality_score: int
    employability_score: int


class ResumeAnalysis(BaseModel):
    sections: ResumeSections
    scores: ScoreBreakdown
    strengths: list[str]
    risks: list[str]
    recommendations: list[str]
    improved_bullets: list[str]


class JobMatchReport(BaseModel):
    match_percentage: int
    missing_skills: list[str]
    keyword_gap: list[str]
    recommendation_report: list[str]
    interview_readiness_score: int


class InterviewQuestionSet(BaseModel):
    role: str
    interview_type: str
    questions: list[str]
    expected_signals: list[str]
    follow_ups: list[str]


class InterviewFeedback(BaseModel):
    feedback_score: int
    confidence: int
    completeness: int
    technical_depth: int
    communication_quality: int
    improvement_areas: list[str]
    ideal_answer: str

