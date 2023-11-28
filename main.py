from fastapi import FastAPI


app = FastAPI()

tasks_data = [
    {"description": "Learn FastAPI", "priority": 3, "is_complete": True},
    {"description": "Do exercises", "priority": 2, "is_complete": False}
]

users_data = [
    {"username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"username": "Andżela", "password": "hasło1!", "is_admin": False},
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
