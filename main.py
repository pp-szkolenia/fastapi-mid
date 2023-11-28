from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random


app = FastAPI()


def get_item_by_id(items_list, id_):
    for item in items_list:
        if item["id"] == id_:
            result = item
            break
    else:
        result = None

    return result


def get_item_index_by_id(items_list, id_):
    for i, item in enumerate(items_list):
        if item["id"] == id_:
            return i


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
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
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hello world"})


@app.get("/tasks/")
def get_tasks():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@app.get("/users/")
def get_users():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})


@app.get("/tasks/{id_}")
def get_task_by_id(id_: int):
    target_task = get_item_by_id(tasks_data, id_)

    if not target_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_task})


@app.get("/users/{id_}")
def get_user_by_id(id_: int):
    target_user = get_item_by_id(users_data, id_)

    if not target_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_user})


@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskBody):
    new_task = body.model_dump()
    random_id = random.randint(1, 10000)
    new_task["id"] = random_id

    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody):
    new_user = body.model_dump()
    random_id = random.randint(1, 10000)
    new_user["id"] = random_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}


@app.delete("/tasks/{id_}")
def delete_task_by_id(id_: int):
    target_index = get_item_index_by_id(tasks_data, id_)

    if target_index is None:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    tasks_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/users/{id_}")
def delete_user_by_id(id_: int):
    target_index = get_item_index_by_id(users_data, id_)

    if target_index is None:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    users_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/users/{id_}")
def update_user_by_id(id_: int, body: UserBody):
    target_index = get_item_index_by_id(users_data, id_)

    if target_index is None:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_user = body.model_dump()
    updated_user["id"] = id_
    users_data[target_index] = updated_user

    message = {"message": f"User with id {id_} updated", "new_value": updated_user}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
