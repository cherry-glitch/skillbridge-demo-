# SkillBridge

A working prototype of the **student-side flow** from the AI-Powered Academia–Industry
Collaboration Platform concept:

```
Register → Assess → Skill Profile ("Skill DNA") → Pick target role → Skill Gap
→ Learning Roadmap → Matched Internships (explainable %) → Apply → Track
```

- `backend/` — FastAPI + SQLite API (auth, assessment engine, skill-gap engine, matching engine)
- `frontend/` — React + Vite + Tailwind student console

## Quick start

**Terminal 1 — backend**
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — frontend**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, register a student account, take the assessment, pick a
target role (try "IoT Engineer"), and walk through Skill Gap → Roadmap → Matches.

The Vite dev server proxies `/api/*` to `http://localhost:8000` (see `frontend/vite.config.js`),
so no CORS setup is needed locally. Full endpoint docs live at `http://localhost:8000/docs`
once the backend is running.

## What's real vs. seeded

- **Real**: auth, assessment scoring, skill-gap math, roadmap generation, internship
  matching, applications — all computed live from what you answer.
- **Seeded (swap-in points for later)**: the question bank, learning resources, and
  internship listings are static seed data (`backend/app/seed_data.py`) standing in for
  where real content, an LMS integration, and live employer postings would go. Resume/LLM
  based skill extraction (doc section 6) isn't wired up yet — `StudentSkill.source` already
  supports a `"resume"` value for when that's added.

## Where this maps to the original concept doc

| Doc section | Here |
|---|---|
| 5.1 AI Skill Assessment & Skill DNA | `/assessment` scoring → `StudentSkill` table |
| 5.2 Skill Gap Analysis | `app/matching.py::skill_gap_for_role` |
| 5.3 Personalized Learning Roadmap | `/students/me/roadmap` |
| 5.4 AI Internship & Job Matching | `app/matching.py::match_for_internship` |
| 5.5 Verified Digital Portfolio | `StudentSkill.source` (assessment/resume/verified) — portfolio UI not yet built |
| 7. System Architecture | Frontend (React) → Backend API (FastAPI) → Auth (JWT) → DB (SQLite→Postgres) → Matching engine |

## Next build targets (not yet started)

- Industry side: post internships/jobs, view ranked candidates
- Institution dashboard: aggregate readiness + skill-demand analytics
- Resume/JD parsing via an LLM to auto-populate `StudentSkill`
- Swap SQLite → Postgres/Supabase for deployment
