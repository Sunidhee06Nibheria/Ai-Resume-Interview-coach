from __future__ import annotations


def resume_report_to_markdown(report: dict) -> str:
    analysis = report["resume_analysis"]
    scores = analysis["scores"]
    lines = [
        "# AI Resume Report",
        "",
        f"Executive summary: {report['executive_summary']}",
        "",
        "## Scores",
        *[f"- {key.replace('_', ' ').title()}: {value}/100" for key, value in scores.items()],
        "",
        "## Recommendations",
        *[f"- {item}" for item in analysis["recommendations"]],
    ]
    return "\n".join(lines)

