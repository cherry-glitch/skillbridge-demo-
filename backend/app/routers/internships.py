from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_student
from ..matching import match_for_internship

router = APIRouter(tags=["internships"])


@router.get("/internships", response_model=List[schemas.InternshipMatchOut])
def list_internships(
    student: models.Student = Depends(get_current_student), db: Session = Depends(get_db)
):
    """
    Every active internship, each annotated with this student's compatibility
    score and an explanation (strong skills vs gap skills) — sorted best
    match first, matching the doc's "compatibility score with reasons".
    """
    internships = db.query(models.Internship).filter(models.Internship.is_active == True).all()  # noqa: E712
    out = []
    for internship in internships:
        match_percent, strong, gap = match_for_internship(db, student, internship)
        out.append(schemas.InternshipMatchOut(
            internship=internship, match_percent=match_percent,
            strong_skills=strong, gap_skills=gap,
        ))
    out.sort(key=lambda x: -x.match_percent)
    return out


@router.post("/internships/{internship_id}/apply", response_model=schemas.ApplicationOut)
def apply_to_internship(
    internship_id: int,
    student: models.Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    internship = db.query(models.Internship).get(internship_id)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    existing = (
        db.query(models.Application)
        .filter(
            models.Application.student_id == student.id,
            models.Application.internship_id == internship_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this internship")

    match_percent, _, _ = match_for_internship(db, student, internship)
    application = models.Application(
        student_id=student.id, internship_id=internship_id,
        status="applied", match_score=match_percent,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/students/me/applications", response_model=List[schemas.ApplicationOut])
def my_applications(
    student: models.Student = Depends(get_current_student), db: Session = Depends(get_db)
):
    return (
        db.query(models.Application)
        .filter(models.Application.student_id == student.id)
        .order_by(models.Application.applied_at.desc())
        .all()
    )
