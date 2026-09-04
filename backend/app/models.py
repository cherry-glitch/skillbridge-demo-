"""
ORM models for the Student-side MVP:

Student  --(assessment)-->  StudentSkill  --compared against-->  RoleSkill (per Role)
Student  --applies to-->  Internship (matched via InternshipSkill overlap)

Kept intentionally flat/simple for a hackathon prototype: one `Skill` table
shared across roles, questions, resources and internships so every part of
the platform is speaking the same "skill taxonomy".
"""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text
)
from sqlalchemy.orm import relationship

from .database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)  # e.g. "Embedded", "Cloud", "Core CS"

    questions = relationship("Question", back_populates="skill")
    resources = relationship("Resource", back_populates="skill")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, default="")

    role_skills = relationship("RoleSkill", back_populates="role")


class RoleSkill(Base):
    """Required skills for a target role, with an importance weight (1-5)."""
    __tablename__ = "role_skills"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    weight = Column(Integer, default=3)  # 1 = nice-to-have, 5 = critical

    role = relationship("Role", back_populates="role_skills")
    skill = relationship("Skill")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    target_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    target_role = relationship("Role")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")


class StudentSkill(Base):
    """A student's current level (0-100) in a given skill, and where it came from."""
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    score = Column(Float, default=0.0)  # 0-100
    source = Column(String, default="assessment")  # assessment | resume | verified | manual
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill")


class Question(Base):
    """A single MCQ tagged to one skill, used to score that skill during assessment."""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)  # "a" | "b" | "c" | "d"
    difficulty = Column(Integer, default=1)  # 1-3, harder questions worth more

    skill = relationship("Skill", back_populates="questions")


class Resource(Base):
    """A learning resource (course/article/practice set) recommended to close a skill gap."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String, nullable=False)
    provider = Column(String, default="")
    url = Column(String, default="")
    resource_type = Column(String, default="course")  # course | project | article | practice
    est_hours = Column(Integer, default=10)

    skill = relationship("Skill", back_populates="resources")


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text, default="")
    location = Column(String, default="Remote")
    stipend = Column(String, default="")
    is_active = Column(Boolean, default=True)

    internship_skills = relationship("InternshipSkill", back_populates="internship")


class InternshipSkill(Base):
    __tablename__ = "internship_skills"

    id = Column(Integer, primary_key=True, index=True)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    weight = Column(Integer, default=3)

    internship = relationship("Internship", back_populates="internship_skills")
    skill = relationship("Skill")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)
    status = Column(String, default="applied")  # applied | shortlisted | rejected | selected
    match_score = Column(Float, default=0.0)
    applied_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="applications")
    internship = relationship("Internship")
