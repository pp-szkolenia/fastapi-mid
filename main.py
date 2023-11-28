from fastapi import FastAPI


app = FastAPI()

tasks_data = [
    {"description": "Learn FastAPI", "priority": 3, "is_complete": True},
    {"description": "Do exercises", "priority": 2, "is_complete": False}
]

@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/tasks/")
def get_tasks():
    return {"result": tasks_data}
