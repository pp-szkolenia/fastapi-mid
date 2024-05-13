from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.models import (UserBody, UserResponse, GetAllUsersResponse, GetSingleUserResponse,
                        PostUserResponse, PutUserResponse, PutUserNoDetailResponse, SortOrders,
                        TokenData)
from app.utils import hash_password_in_body
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from db.orm import get_session
from db.models import UserTable
from app import oauth2


router = APIRouter()


@router.get("/users/", tags=["users"], response_model=GetAllUsersResponse)
def get_users(session: Session = Depends(get_session), is_admin: bool | None = None,
              password_limit: int | None = None, sort_username: SortOrders = None,
              user_data: TokenData = Depends(oauth2.get_current_user)):
    if not user_data.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform this operation")

    users_data = session.query(UserTable)
    if is_admin is not None:
        users_data = users_data.filter_by(is_admin=is_admin)

    if password_limit is not None:
        users_data = users_data.filter(func.length(UserTable.password) <= password_limit)

    if sort_username is not None:
        if sort_username == SortOrders.ASCENDING:
            sort_func = asc
        elif sort_username == SortOrders.DESCENDING:
            sort_func = desc

        users_data = users_data.order_by(sort_func(UserTable.username))

    users_data = users_data.all()

    users_data = [UserResponse(id_=user.id_number,
                               username=user.username,
                               password=user.password,
                               is_admin=user.is_admin)
                  for user in users_data]

    return {"result": users_data}


@router.get("/users/{id_}", tags=["users"], response_model=GetSingleUserResponse)
def get_user_by_id(id_: int, session: Session = Depends(get_session),
                   user_data: TokenData = Depends(oauth2.get_current_user)):
    if not user_data.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform this operation")

    target_user = session.query(UserTable).filter_by(id_number=id_).first()

    if not target_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    target_user = UserResponse(id_=target_user.id_number,
                               username=target_user.username,
                               password=target_user.password,
                               is_admin=target_user.is_admin)

    return {"result": target_user}


@router.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"],
             response_model=PostUserResponse)
def create_user(body: UserBody, session: Session = Depends(get_session)):
    body = hash_password_in_body(body)

    user_dict = body.model_dump()
    new_user = UserTable(**user_dict)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    new_user = UserResponse(id_=new_user.id_number, username=new_user.username,
                            password=new_user.password, is_admin=new_user.is_admin)

    return {"message": "New user added", "details": new_user}


@router.delete("/users/{id_}", tags=["users"])
def delete_user_by_id(id_: int, session: Session = Depends(get_session),
                      user_data: TokenData = Depends(oauth2.get_current_user)):

    if not (user_data.is_admin or user_data.user_id == id_):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this operation")

    deleted_user = session.query(UserTable).filter_by(id_number=id_).first()

    if not deleted_user:
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    session.delete(deleted_user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{id_}", tags=["users"], response_model=PutUserResponse | PutUserNoDetailResponse)
def update_user_by_id(id_: int, body: UserBody, session: Session = Depends(get_session),
                      show_user: bool = True, user_data: TokenData = Depends(oauth2.get_current_user)):
    if not (user_data.is_admin or user_data.user_id == id_):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this operation")

    filter_query = session.query(UserTable).filter_by(id_number=id_)

    if not filter_query.first():
        message = {"error": f"User with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    body = hash_password_in_body(body)

    filter_query.update(body.model_dump())
    session.commit()

    updated_user = filter_query.first()

    updated_user = UserResponse(id_=updated_user.id_number, username=updated_user.username,
                                password=updated_user.password, is_admin=updated_user.is_admin)

    if show_user:
        message = {"message": f"User with id {id_} updated", "new_value": updated_user}
    else:
        message = {"message": f"User with id {id_} updated"}

    return message
