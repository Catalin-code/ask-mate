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
    query = """
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


@connection.connection_handler
def get_questions_by_user_id(cursor, user_id):
    query = f"""
        SELECT * FROM question
        WHERE user_id = {user_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_user_id(cursor, user_id):
    query = f"""
        SELECT * FROM answer
        WHERE user_id = {user_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_user_id(cursor, user_id):
    query = f"""
        SELECT * FROM comment
        WHERE user_id = {user_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def accept_answer(cursor, answer_id, user_id):
    query = f"""
        UPDATE answer
        SET accepted = true
        WHERE id = {answer_id}
    """
    cursor.execute(query)
    query_for_reputation_gain = f"""
        UPDATE "user"
        SET reputation = reputation + 15
        WHERE user_id = {user_id}
    """
    cursor.execute(query_for_reputation_gain)


@connection.connection_handler
def unaccept_answer(cursor, answer_id):
    query = f"""
        UPDATE answer
        SET accepted = false
        WHERE id = {answer_id}
    """
    cursor.execute(query)


@connection.connection_handler
def get_tags(cursor):
    query = """
        SELECT * FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()
