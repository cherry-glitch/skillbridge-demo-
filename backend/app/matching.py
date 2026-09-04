"""
Core "AI" logic for the prototype.

For the SIH MVP this is a transparent, explainable weighted-overlap model
rather than a black-box ML model — which matches the doc's requirement
that recommendations be "explainable rather than a simple list". It's a
clean seam to later swap in a trained model without touching callers.
"""
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from . import models

HAVE_THRESHOLD = 60.0  # score (0-100) at/above which we say the student "has" a skill


def get_student_score_map(db: Session, student_id: int) -> Dict[int, float]:
    rows = db.query(models.StudentSkill).filter(models.StudentSkill.student_id == student_id).all()
    return {row.skill_id: row.score for row in rows}


def skill_gap_for_role(db: Session, student: models.Student, role: models.Role):
    score_map = get_student_score_map(db, student.id)
    strong, gap = [], []
    weighted_sum, weight_total = 0.0, 0

    for rs in role.role_skills:
        score = score_map.get(rs.skill_id, 0.0)
        has_it = score >= HAVE_THRESHOLD
        item = {
            "skill": rs.skill,
            "required_weight": rs.weight,
            "student_score": score,
            "has_skill": has_it,
            "gap_size": 0.0 if has_it else round(HAVE_THRESHOLD - score, 1),
        }
        (strong if has_it else gap).append(item)

        weighted_sum += rs.weight * min(score, 100.0) / 100.0
        weight_total += rs.weight

    readiness = round((weighted_sum / weight_total) * 100, 1) if weight_total else 0.0
    # Sort gaps by importance (highest weight, biggest shortfall first) — this
    # ordering drives the roadmap priority too.
    gap.sort(key=lambda x: (-x["required_weight"], -x["gap_size"]))
    strong.sort(key=lambda x: -x["required_weight"])
    return strong, gap, readiness


def match_for_internship(db: Session, student: models.Student, internship: models.Internship):
    score_map = get_student_score_map(db, student.id)
    strong, gap = [], []
    weighted_sum, weight_total = 0.0, 0

    for isk in internship.internship_skills:
        score = score_map.get(isk.skill_id, 0.0)
        matched = score >= HAVE_THRESHOLD
        detail = {"skill": isk.skill, "student_score": score, "matched": matched}
        (strong if matched else gap).append(detail)

        weighted_sum += isk.weight * min(score, 100.0) / 100.0
        weight_total += isk.weight

    match_percent = round((weighted_sum / weight_total) * 100, 1) if weight_total else 0.0
    return match_percent, strong, gap
