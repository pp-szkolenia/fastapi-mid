from passlib.context import CryptContext

from app.models import UserBody


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password_in_body(user_body: UserBody):
    user_body.password = pwd_context.hash(user_body.password)
    return user_body


def verify(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)
