from fastapi import FastAPI, Body
from pydantic import BaseModel
import random


app = FastAPI()


class TaskBody(BaseModel):
    description: str
    priority: int | None = None  # < 3.10 -> priority: Optional[int] = None
    is_complete: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_complete": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_complete": False}
]

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False},
]


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/tasks/")
def get_tasks():
    return {"result": tasks_data}


@app.get("/users/")
def get_users():
    return {"result": users_data}


@app.post("/tasks/")
def create_task(body: TaskBody):
    new_task = body.model_dump()
    random_id = random.randint(1, 10000)  # low probability of duplication
    new_task["id"] = random_id

    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}


@app.post("/users/")
def create_user(body: UserBody):
    new_user = body.model_dump()
    random_id = random.randint(1, 10000)
    new_user["id"] = random_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}
