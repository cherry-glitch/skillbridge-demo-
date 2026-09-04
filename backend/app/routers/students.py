from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_student
from ..matching import skill_gap_for_role

router = APIRouter(prefix="/students/me", tags=["student"])


@router.get("", response_model=schemas.StudentOut)
def get_profile(student: models.Student = Depends(get_current_student)):
    return student


@router.get("/skills", response_model=List[schemas.StudentSkillOut])
def get_skill_profile(
    student: models.Student = Depends(get_current_student), db: Session = Depends(get_db)
):
    rows = (
        db.query(models.StudentSkill)
        .filter(models.StudentSkill.student_id == student.id)
        .join(models.Skill)
        .order_by(models.Skill.category, models.Skill.name)
        .all()
    )
    return rows


@router.post("/target-role", response_model=schemas.StudentOut)
def set_target_role(
    payload: schemas.TargetRoleIn,
    student: models.Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    role = db.query(models.Role).get(payload.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    student.target_role_id = role.id
    db.commit()
    db.refresh(student)
    return student


@router.get("/skill-gap", response_model=schemas.SkillGapOut)
def get_skill_gap(
    student: models.Student = Depends(get_current_student), db: Session = Depends(get_db)
):
    if not student.target_role_id:
        raise HTTPException(status_code=400, detail="Select a target role first")
    role = db.query(models.Role).get(student.target_role_id)
    strong, gap, readiness = skill_gap_for_role(db, student, role)
    return schemas.SkillGapOut(role=role, strong_skills=strong, gap_skills=gap, readiness_percent=readiness)


@router.get("/roadmap", response_model=schemas.RoadmapOut)
def get_roadmap(
    student: models.Student = Depends(get_current_student), db: Session = Depends(get_db)
):
    if not student.target_role_id:
        raise HTTPException(status_code=400, detail="Select a target role first")
    role = db.query(models.Role).get(student.target_role_id)
    _, gap, _ = skill_gap_for_role(db, student, role)

    items = []
    total_hours = 0
    for gap_item in gap:
        resources = (
            db.query(models.Resource)
            .filter(models.Resource.skill_id == gap_item["skill"].id)
            .all()
        )
        total_hours += sum(r.est_hours for r in resources)
        items.append(schemas.RoadmapItem(skill=gap_item["skill"], resources=resources))

    return schemas.RoadmapOut(role=role, items=items, total_est_hours=total_hours)
