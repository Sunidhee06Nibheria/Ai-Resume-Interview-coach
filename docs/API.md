# API Documentation

Run:

```powershell
uvicorn backend.main:app --reload --port 8000
```

Open:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

## Endpoints

### `POST /api/analyze-resume`

Multipart form with `file`.

Returns full resume analysis, ATS report, skill gap report, and career plan.

### `POST /api/match-job`

Multipart form with `file` and `job_description`.

Returns match percentage, missing skills, keyword gaps, recommendations, and interview readiness.

### `POST /api/interview/questions`

Form fields:

- `role`
- `interview_type`

Returns generated questions, expected signals, and follow-ups.

### `POST /api/interview/feedback`

Form fields:

- `question`
- `answer`
- `role`

Returns feedback score and rubric breakdown.

