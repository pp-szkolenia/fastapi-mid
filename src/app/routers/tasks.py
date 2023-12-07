from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from app.models import TaskBody
from db.utils import connect_to_db


router = APIRouter()


@router.get("/tasks/", tags=["tasks"])
def get_tasks():
    conn, cursor = connect_to_db()

    cursor.execute("SELECT * FROM tasks")
    tasks_data = cursor.fetchall()

    conn.close()
    cursor.close()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@router.get("/tasks/{id_}", tags=["tasks"])
def get_task_by_id(id_: int):
    conn, cursor = connect_to_db()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id_,))
    target_task = cursor.fetchone()

    conn.close()
    cursor.close()

    if not target_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_task})


@router.post("/tasks/", status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(body: TaskBody):
    conn, cursor = connect_to_db()

    insert_query_template = f"""INSERT INTO tasks (description, priority, is_complete)
                                 VALUES (%s, %s, %s) RETURNING *"""
    insert_query_values = (body.description, body.priority, body.is_complete)

    cursor.execute(insert_query_template, insert_query_values)
    new_task = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    return {"message": "New task added", "details": new_task}


@router.delete("/tasks/{id_}", tags=["tasks"])
def delete_task_by_id(id_: int):
    conn, cursor = connect_to_db()

    delete_query = f"DELETE FROM tasks WHERE id=%s RETURNING *"

    cursor.execute(delete_query, (id_,))
    deleted_post = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not deleted_post:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{id_}", tags=["tasks"])
def update_task_by_id(id_: int, body: TaskBody):
    conn, cursor = connect_to_db()

    update_query_template = f"""UPDATE tasks SET description=%s, priority=%s, is_complete=%s
                                WHERE id=%s RETURNING *"""
    update_query_values = (body.description, body.priority, body.is_complete, id_)

    cursor.execute(update_query_template, update_query_values)
    updated_task = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not updated_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    message = {"message": f"Task with id {id_} updated", "new_value": updated_task}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
