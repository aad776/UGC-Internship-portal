

from pydantic import BaseModel
from typing import List, Optional


class Student(BaseModel):
    id: int
    name: str
    year: int
    department: str
    skills: List[str]
    interests: List[str]
    preferred_location: str


class Internship(BaseModel):
    id: int
    company: str
    title: str
    required_skills: List[str]
    location: str
    mode: str


class Application(BaseModel):
    student_id: int
    internship_id: int
    status: str = "Applied"


class ApplyRequest(BaseModel):
    student_id: int
    internship_id: int
