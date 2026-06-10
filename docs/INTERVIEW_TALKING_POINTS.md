# How To Discuss This Project In Interviews

## Strong Pitch

I built an AI career copilot that combines document parsing, explainable scoring, RAG, and task-specific agents to help users improve resumes and prepare for interviews. I designed it so the app works offline with deterministic fallbacks, but can be upgraded to Gemini or any OpenAI-compatible model provider.

## Architectural Decisions

- I separated agents by responsibility to avoid one giant prompt or service.
- I used Pydantic outputs so reports are predictable and UI-friendly.
- I kept scoring explainable because career recommendations need user trust.
- I made the RAG layer resilient with local fallback embeddings.
- I built both FastAPI and Streamlit to show production API thinking and product UX.

## Recruiter Expectations

Recruiters and hiring managers want evidence of shipped work, measurable thinking, clean architecture, and the ability to explain tradeoffs. This project gives you concrete stories around orchestration, retrieval, evaluation, and product design.

