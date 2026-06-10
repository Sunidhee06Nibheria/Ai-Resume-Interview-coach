from __future__ import annotations


class ReportAgent:
    name = "report-agent"

    def assemble(self, payload: dict) -> dict:
        scores = payload.get("resume_analysis", {}).get("scores", {})
        summary = "Resume is ready for targeted improvement."
        if scores.get("resume_score", 0) >= 80:
            summary = "Resume is strong and close to recruiter-ready."
        elif scores.get("resume_score", 0) < 55:
            summary = "Resume needs clearer structure, keywords, and measurable impact."
        return {"executive_summary": summary, **payload}

