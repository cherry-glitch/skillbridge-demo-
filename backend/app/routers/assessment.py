from collections import defaultdict
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_student

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.get("/questions", response_model=List[schemas.QuestionOut])
def get_questions(skill_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Returns the question bank (optionally filtered to one skill).
    `correct_option` is excluded by the response schema.
    """
    query = db.query(models.Question)
    if skill_id is not None:
        query = query.filter(models.Question.skill_id == skill_id)
    return query.all()


@router.post("/submit", response_model=schemas.AssessmentResultOut)
def submit_assessment(
    payload: schemas.AssessmentSubmission,
    db: Session = Depends(get_db),
    student: models.Student = Depends(get_current_student),
):
    """
    Scores each answered skill as (correct / total_answered_for_that_skill) * 100,
    then upserts a StudentSkill row per skill so the profile always reflects
    the latest assessment attempt.
    """
    question_ids = [a.question_id for a in payload.answers]
    questions = {
        q.id: q for q in db.query(models.Question).filter(models.Question.id.in_(question_ids)).all()
    }

    per_skill_correct = defaultdict(int)
    per_skill_total = defaultdict(int)

    for answer in payload.answers:
        question = questions.get(answer.question_id)
        if not question:
            continue
        per_skill_total[question.skill_id] += 1
        if answer.selected_option.lower() == question.correct_option.lower():
            per_skill_correct[question.skill_id] += 1

    results = []
    for skill_id, total in per_skill_total.items():
        correct = per_skill_correct[skill_id]
        score = round((correct / total) * 100, 1) if total else 0.0

        existing = (
            db.query(models.StudentSkill)
            .filter(
                models.StudentSkill.student_id == student.id,
                models.StudentSkill.skill_id == skill_id,
            )
            .first()
        )
        if existing:
            existing.score = score
            existing.source = "assessment"
        else:
            db.add(models.StudentSkill(
                student_id=student.id, skill_id=skill_id, score=score, source="assessment",
            ))

        skill = db.query(models.Skill).get(skill_id)
        results.append(schemas.SkillResultOut(skill=skill, correct=correct, total=total, score=score))

    db.commit()
    return schemas.AssessmentResultOut(results=results)
