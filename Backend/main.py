from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from database.repository import init_db


app = FastAPI(
    title="AI Resume & Interview Coach API",
    version="1.0.0",
    description="Agentic AI backend for resume analysis, ATS scoring, career coaching, and interview simulation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(router, prefix="/api")


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "AI Resume & Interview Coach"}

