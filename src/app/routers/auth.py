from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session
from db.models import UserTable
from db.orm import get_session
from app.models import UserLogin, Token
from app import utils, oauth2


router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    user = session.query(UserTable).filter(UserTable.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    payload = {"user_id": user.id_number, "is_admin": user.is_admin}
    access_token = oauth2.create_access_token(data=payload)
    return {"access_token": access_token, "token_type": "bearer"}
