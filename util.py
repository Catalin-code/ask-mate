from flask_bcrypt import bcrypt
import connection
from psycopg2.extras import RealDictCursor


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def add_user(email: str, password: str, date: str, cursor: RealDictCursor) -> list:
    query = """
        INSERT INTO user(email, password, date)
        VALUES ({email}, {password}, {date})
        """
    cursor.execute(query)
