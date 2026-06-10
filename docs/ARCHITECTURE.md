# Architecture

The project is organized around separation of concerns:

- Streamlit owns the product workflow and visual analytics.
- FastAPI exposes production-friendly endpoints.
- Parsers convert PDF, DOCX, and TXT files into clean text.
- Agents own task-specific reasoning.
- Workflows coordinate agents into a multi-step AI system.
- RAG retrieves resume, interview, and career best-practice context.
- SQLite stores analyses and supports future product analytics.

## Agent Responsibilities

- Resume Agent: extracts sections, scores profile quality, identifies strengths and risks.
- ATS Agent: finds keyword gaps, formatting issues, weak bullets, and action verbs.
- Career Agent: recommends career paths, projects, internships, and certifications.
- Skill Gap Agent: compares current profile with target role requirements.
- Interview Agent: generates interview questions and evaluates user answers.
- Report Agent: assembles a user-facing executive summary.

## LangGraph Workflow

The workflow is intentionally implemented as a simple orchestration boundary in `workflows/career_workflow.py`. This keeps local execution reliable while preserving the structure needed to migrate to a formal LangGraph state graph:

1. Resume analysis
2. ATS optimization
3. Skill gap analysis
4. Career coaching
5. Report assembly

## RAG Pipeline

The RAG layer chunks career knowledge, embeds it, retrieves top matches, and injects that context into agent recommendations. It uses `sentence-transformers` when available and falls back to deterministic hash embeddings for offline demos.

