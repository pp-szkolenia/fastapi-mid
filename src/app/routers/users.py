from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
import random

from app.utils import get_item_by_id, get_item_index_by_id
from app.models import UserBody


router = APIRouter()

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False},
]


@router.get("/users/", tags=["users"])
def get_users():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})


@router.get("/users/{id_}", tags=["users"])
def get_user_by_id(id_: int):
    target_user = get_item_by_id(users_data, id_)

    if not target_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_user})


@router.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(body: UserBody):
    new_user = body.model_dump()
    random_id = random.randint(1, 10000)
    new_user["id"] = random_id

    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}


@router.delete("/users/{id_}", tags=["users"])
def delete_user_by_id(id_: int):
    target_index = get_item_index_by_id(users_data, id_)

    if target_index is None:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    users_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{id_}", tags=["users"])
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
