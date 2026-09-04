from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, SessionLocal
from .seed_data import seed_if_empty
from .routers import auth, skills, assessment, students, internships

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_if_empty(db)

app = FastAPI(
    title="SkillBridge API",
    description="AI-powered Academia-Industry Collaboration Platform — student-side MVP API.",
    version="0.1.0",
)

# Wide open for local prototype/demo use. Lock this down to your real
# frontend origin before deploying anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(assessment.router)
app.include_router(students.router)
app.include_router(internships.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "SkillBridge API", "docs": "/docs"}
