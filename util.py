from flask_bcrypt import bcrypt
import connection
from psycopg2.extras import RealDictCursor
from datetime import datetime
from time import time


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_current_time():
    return datetime.fromtimestamp(int(time())).strftime("%Y-%m-%d %H:%M:%S")


@connection.connection_handler
def add_user(cursor, email, password, date):
    query = f"""
        INSERT INTO "user" (username, password, date, questions, answers, comments, reputation)
        VALUES ('{email}', '{password}', '{date}', 0, 0, 0, 0)

        """
    cursor.execute(query)


@connection.connection_handler
def list_users(cursor):
    query = f"""
        SELECT * FROM "user"
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_user_by_id(cursor, user_id):
    query = f"""
        SELECT * FROM "user"
        WHERE user_id = {user_id}
    """
    cursor.execute(query)
    return cursor.fetchall()
