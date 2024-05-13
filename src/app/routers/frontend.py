from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.models import TaskResponse, TokenData
from sqlalchemy.orm import Session
from db.orm import get_session
from db.models import TaskTable
from app import oauth2


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request})


@router.get("/signup/")
def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/tasks-list/")
def list_tasks(request: Request, session: Session = Depends(get_session)):

    tasks_data = [
        dict(TaskResponse(id_=task.id_number,
                          description=task.description,
                          priority=task.priority,
                          is_complete=task.is_complete))
        for task in session.query(TaskTable).all()]

    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks_data})
