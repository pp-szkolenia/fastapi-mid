from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import JSONResponse

from app.models import TaskBody
from sqlalchemy.orm import Session
from db.orm import get_session
from db.models import TaskTable


router = APIRouter()


@router.get("/tasks/", tags=["tasks"])
def get_tasks(session: Session = Depends(get_session)):
    tasks_data = session.query(TaskTable).all()

    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})  # error
    return {"result": tasks_data}


@router.get("/tasks/{id_}", tags=["tasks"])
def get_task_by_id(id_: int, session: Session = Depends(get_session)):
    target_task = session.query(TaskTable).filter_by(id_number=id_).first()

    if not target_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_task})  # error
    return {"result": target_task}


@router.post("/tasks/", status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(body: TaskBody, session: Session = Depends(get_session)):
    task_dict = body.model_dump()
    new_task = TaskTable(**task_dict)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

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


@router.put("/tasks/{id_}", tags=["tasks"])
def update_task_by_id(id_: int, body: TaskBody, session: Session = Depends(get_session)):
    filter_query = session.query(TaskTable).filter_by(id_number=id_)

    if not filter_query.first():
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    filter_query.update(body.model_dump())
    session.commit()

    updated_task = filter_query.first()

    message = {"message": f"Task with id {id_} updated", "new_value": updated_task}
    # return JSONResponse(status_code=status.HTTP_200_OK, content=message) # error
    return message
