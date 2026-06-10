from __future__ import annotations

import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

DB_PATH = Path(os.getenv("DATABASE_URL", "database/career_copilot.sqlite3"))


def connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                raw_text TEXT NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                feedback_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS learning_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                desired_role TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def save_resume_analysis(filename: str, raw_text: str, report: dict) -> int:
    init_db()
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO resume_analyses (filename, raw_text, report_json, created_at) VALUES (?, ?, ?, ?)",
            (filename, raw_text, json.dumps(report), datetime.now(UTC).isoformat()),
        )
        return int(cursor.lastrowid)


def list_resume_analyses(limit: int = 20) -> list[dict]:
    init_db()
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, filename, report_json, created_at FROM resume_analyses ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "filename": row["filename"],
            "report": json.loads(row["report_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]

