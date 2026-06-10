# Deployment Guide

## Streamlit Cloud

1. Push the repository to GitHub.
2. Create a new Streamlit app.
3. Set main file to `app.py`.
4. Add secrets from `.env.example` if using hosted LLMs.

## Render or Railway

For the API:

```powershell
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

For the dashboard:

```powershell
streamlit run app.py --server.address 0.0.0.0
```

## Docker

```powershell
docker compose up --build
```

The Streamlit app will be available on `http://localhost:8501`.

