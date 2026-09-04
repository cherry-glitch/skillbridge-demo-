from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class StudentLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    target_role_id: Optional[int] = None

    class Config:
        from_attributes = True


# ---------- Skills / Roles ----------

class SkillOut(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True


class RoleOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class StudentSkillOut(BaseModel):
    skill: SkillOut
    score: float
    source: str

    class Config:
        from_attributes = True


# ---------- Assessment ----------

class QuestionOut(BaseModel):
    id: int
    skill_id: int
    prompt: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    # NOTE: correct_option intentionally omitted from the response schema
    # so it's never sent to the client.

    class Config:
        from_attributes = True


class AnswerIn(BaseModel):
    question_id: int
    selected_option: str  # "a" | "b" | "c" | "d"


class AssessmentSubmission(BaseModel):
    answers: List[AnswerIn]


class SkillResultOut(BaseModel):
    skill: SkillOut
    correct: int
    total: int
    score: float  # 0-100


class AssessmentResultOut(BaseModel):
    results: List[SkillResultOut]


# ---------- Skill gap / roadmap ----------

class SkillGapItem(BaseModel):
    skill: SkillOut
    required_weight: int
    student_score: float
    has_skill: bool  # True if student_score crosses the "have it" threshold
    gap_size: float  # 0 if has_skill else magnitude of the shortfall


class SkillGapOut(BaseModel):
    role: RoleOut
    strong_skills: List[SkillGapItem]
    gap_skills: List[SkillGapItem]
    readiness_percent: float


class ResourceOut(BaseModel):
    id: int
    skill_id: int
    title: str
    provider: str
    url: str
    resource_type: str
    est_hours: int

    class Config:
        from_attributes = True


class RoadmapItem(BaseModel):
    skill: SkillOut
    resources: List[ResourceOut]


class RoadmapOut(BaseModel):
    role: RoleOut
    items: List[RoadmapItem]
    total_est_hours: int


# ---------- Internships / matching ----------

class InternshipOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    location: str
    stipend: str

    class Config:
        from_attributes = True


class MatchSkillDetail(BaseModel):
    skill: SkillOut
    student_score: float
    matched: bool


class InternshipMatchOut(BaseModel):
    internship: InternshipOut
    match_percent: float
    strong_skills: List[MatchSkillDetail]
    gap_skills: List[MatchSkillDetail]


class ApplicationOut(BaseModel):
    id: int
    internship: InternshipOut
    status: str
    match_score: float
    applied_at: datetime

    class Config:
        from_attributes = True


class TargetRoleIn(BaseModel):
    role_id: int
