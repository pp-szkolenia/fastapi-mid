from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
import random

from app.utils import get_item_by_id, get_item_index_by_id
from app.models import TaskBody


router = APIRouter()

tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_complete": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_complete": False}
]


@router.get("/tasks/")
def get_tasks():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@router.get("/tasks/{id_}")
def get_task_by_id(id_: int):
    target_task = get_item_by_id(tasks_data, id_)

    if not target_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_task})


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskBody):
    new_task = body.model_dump()
    random_id = random.randint(1, 10000)
    new_task["id"] = random_id

    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}


@router.delete("/tasks/{id_}")
def delete_task_by_id(id_: int):
    target_index = get_item_index_by_id(tasks_data, id_)

    if target_index is None:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    tasks_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{id_}")
def update_task_by_id(id_: int, body: TaskBody):
    target_index = get_item_index_by_id(tasks_data, id_)

    if target_index is None:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_task = body.model_dump()
    updated_task["id"] = id_
    tasks_data[target_index] = updated_task

    message = {"message": f"Task with id {id_} updated", "new_value": updated_task}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
