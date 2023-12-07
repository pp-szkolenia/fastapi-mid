from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from app.models import UserBody
from db.utils import connect_to_db


router = APIRouter()


@router.get("/users/", tags=["users"])
def get_users():
    conn, cursor = connect_to_db()

    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()

    conn.close()
    cursor.close()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})


@router.get("/users/{id_}", tags=["users"])
def get_user_by_id(id_: int):
    conn, cursor = connect_to_db()

    cursor.execute("SELECT * FROM users WHERE id = %s", (id_,))
    target_user = cursor.fetchone()

    conn.close()
    cursor.close()

    if not target_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_user})


@router.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(body: UserBody):
    conn, cursor = connect_to_db()

    insert_query_template = f"""INSERT INTO users (username, password, is_admin)
                                     VALUES (%s, %s, %s) RETURNING *"""
    insert_query_values = (body.username, body.password, body.is_admin)

    cursor.execute(insert_query_template, insert_query_values)
    new_user = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    return {"message": "New user added", "details": new_user}


@router.delete("/users/{id_}", tags=["users"])
def delete_user_by_id(id_: int):
    conn, cursor = connect_to_db()

    delete_query = f"DELETE FROM users WHERE id=%s RETURNING *"

    cursor.execute(delete_query, (id_,))
    deleted_user = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not deleted_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{id_}", tags=["users"])
def update_user_by_id(id_: int, body: UserBody):
    conn, cursor = connect_to_db()

    update_query_template = f"""UPDATE users SET username=%s, password=%s, is_admin=%s
                                WHERE id=%s RETURNING *"""
    update_query_values = (body.username, body.password, body.is_admin, id_)

    cursor.execute(update_query_template, update_query_values)
    updated_user = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not updated_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    message = {"message": f"User with id {id_} updated", "new_value": updated_user}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
