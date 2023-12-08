from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from db.utils import get_connection_string


connection_string = get_connection_string()
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
