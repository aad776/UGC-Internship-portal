

from fastapi import FastAPI, HTTPException
from typing import Optional

from data import students, internships, applications
from models import ApplyRequest
from matcher import match_internships

app = FastAPI(title="Internship Finder Portal")




@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")



@app.get("/internships")
def get_internships(skill: Optional[str] = None):
    if skill:
        return [
            i for i in internships
            if skill.lower() in [s.lower() for s in i["required_skills"]]
        ]
    return internships


@app.get("/internships/{internship_id}")
def get_internship(internship_id: int):
    for internship in internships:
        if internship["id"] == internship_id:
            return internship
    raise HTTPException(status_code=404, detail="Internship not found")



@app.get("/match/{student_id}")
def recommend_internships(student_id: int):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return match_internships(student, internships)




@app.post("/apply")
def apply_internship(request: ApplyRequest):
    if not any(s["id"] == request.student_id for s in students):
        raise HTTPException(status_code=404, detail="Student not found")

    if not any(i["id"] == request.internship_id for i in internships):
        raise HTTPException(status_code=404, detail="Internship not found")

    for app in applications:
        if app["student_id"] == request.student_id and app["internship_id"] == request.internship_id:
            raise HTTPException(status_code=400, detail="Already applied")

    applications.append({
        "student_id": request.student_id,
        "internship_id": request.internship_id,
        "status": "Applied"
    })

    return {"message": "Application submitted successfully"}



@app.get("/applications/{student_id}")
def get_applications(student_id: int):
    student_apps = [
        app for app in applications if app["student_id"] == student_id
    ]
    return student_apps
