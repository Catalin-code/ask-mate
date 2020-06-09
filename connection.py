import psycopg2
import psycopg2.extras


connections = {}


def get_connection_string():
    user_name = 'catalin'
    password = '123456'
    host = 'localhost'
    database_name = 'test_db'

    env_variables_defined = True

    if env_variables_defined:
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def connect_database(connection_string):
    try:
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
        return connection
    except psycopg2.DatabaseError as exception:
        print(exception)


def get_cursor():
    connection_string = get_connection_string()
    connection = connect_database(connection_string)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    global connections
    connections[cursor] = connection
    return cursor


def close_connection(cursor):
    connection = connections.get(cursor)
    cursor.close()
    if connection:
        del connections[cursor]
        connection.close()
