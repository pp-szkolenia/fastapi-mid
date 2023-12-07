import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


def get_db_credentials():
    load_dotenv()
    return {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "database": os.environ["DB_NAME"]
    }


def get_connection_string():
    credentials = get_db_credentials()
    user = credentials["user"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    database = credentials["database"]

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def connect_to_db():
    credentials = get_db_credentials()

    connection = psycopg2.connect(**credentials, cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    return connection, cursor
