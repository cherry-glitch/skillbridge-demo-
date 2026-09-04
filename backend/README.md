# SkillBridge — Backend (FastAPI)

Student-side MVP API for the AI-powered Academia–Industry Collaboration Platform.

## What's implemented

- **Auth**: student register/login (JWT bearer tokens)
- **Skill taxonomy & roles**: seeded on first run (IoT Engineer, Software Developer, Data Analyst)
- **Assessment engine**: MCQ question bank tagged per skill → scores each skill 0–100
- **Skill profile**: a student's current score per skill ("Skill DNA")
- **Skill-gap engine**: compares a student's profile against a chosen target role, weighted by skill importance, returns strong skills + gaps + a readiness %
- **Roadmap**: recommends learning resources for each gap skill, ordered by importance
- **Internship matching**: weighted compatibility score per internship with an explanation (strong skills / gap skills) — sorted best match first
- **Applications**: apply to an internship, view your application history

The matching/skill-gap logic (`app/matching.py`) is a transparent, explainable
weighted-overlap model — intentionally not a black box, and a clean seam to
later swap in a trained ML model without touching any callers.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The database (SQLite file `skillbridge.db`) and all seed data (skills, roles,
questions, resources, internships) are created automatically on first run.

- API: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs

## Trying it via /docs

1. `POST /auth/register` — create a student
2. `POST /auth/login` — get a bearer token (use the "Authorize" button in `/docs`)
3. `GET /assessment/questions` — fetch the question bank
4. `POST /assessment/submit` — submit answers (see `AssessmentSubmission` schema)
5. `GET /roles` — pick a target role id
6. `POST /students/me/target-role` — set it
7. `GET /students/me/skill-gap` — see strong skills vs gaps + readiness %
8. `GET /students/me/roadmap` — get recommended resources for the gaps
9. `GET /internships` — see match % + reasons per internship
10. `POST /internships/{id}/apply` — apply

## Moving beyond the prototype

- Swap `SQLALCHEMY_DATABASE_URL` in `app/database.py` for Postgres/Supabase — no other code changes needed.
- Replace the MCQ-only assessment with resume/LLM-based skill extraction (doc section 6, "NLP/LLM") by writing extracted skills into `StudentSkill` with `source="resume"`.
- `app/matching.py` is where a trained recommendation/matching model would plug in later.
