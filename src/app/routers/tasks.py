from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import JSONResponse

from app.models import (TaskBody, TaskResponse, GetSingleTaskResponse, GetAllTasksResponse,
                        PostTaskResponse, PutTaskResponse)
from sqlalchemy.orm import Session
from db.orm import get_session
from db.models import TaskTable


router = APIRouter()


@router.get("/tasks/", tags=["tasks"], response_model=GetAllTasksResponse)
def get_tasks(session: Session = Depends(get_session)):
    tasks_data = session.query(TaskTable).all()

    tasks_data = [
        TaskResponse(id_=task.id_number,
                     description=task.description,
                     priority=task.priority,
                     is_complete=task.is_complete)
        for task in tasks_data]

    return {"result": tasks_data}


@router.get("/tasks/{id_}", tags=["tasks"], response_model=GetSingleTaskResponse)
def get_task_by_id(id_: int, session: Session = Depends(get_session)):
    target_task = session.query(TaskTable).filter_by(id_number=id_).first()

    if not target_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    target_task = TaskResponse(id_=target_task.id_number,
                               description=target_task.description,
                               priority=target_task.priority,
                               is_complete=target_task.is_complete)

    return {"result": target_task}


@router.post("/tasks/", status_code=status.HTTP_201_CREATED, tags=["tasks"],
             response_model=PostTaskResponse)
def create_task(body: TaskBody, session: Session = Depends(get_session)):
    task_dict = body.model_dump()
    new_task = TaskTable(**task_dict)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    new_task = TaskResponse(id_=new_task.id_number,
                            description=new_task.description,
                            priority=new_task.priority,
                            is_complete=new_task.is_complete)

    return {"message": "New task added", "details": new_task}


@router.delete("/tasks/{id_}", tags=["tasks"])
def delete_task_by_id(id_: int, session: Session = Depends(get_session)):
    deleted_task = session.query(TaskTable).filter_by(id_number=id_).first()

    if not deleted_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    session.delete(deleted_task)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{id_}", tags=["tasks"], response_model=PutTaskResponse)
def update_task_by_id(id_: int, body: TaskBody, session: Session = Depends(get_session)):
    filter_query = session.query(TaskTable).filter_by(id_number=id_)

    if not filter_query.first():
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    filter_query.update(body.model_dump())
    session.commit()

    updated_task = filter_query.first()

    updated_task = TaskResponse(id_=updated_task.id_number,
                                description=updated_task.description,
                                priority=updated_task.priority,
                                is_complete=updated_task.is_complete)

    message = {"message": f"Task with id {id_} updated", "new_value": updated_task}

    return message
