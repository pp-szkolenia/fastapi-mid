from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "bc714fc37a3e6f18aa8e3dbce9cb5c9bebf1c7b48fd338472d119d52967a583e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
