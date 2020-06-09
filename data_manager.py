from datetime import datetime
import connection


# Example usage
# print(Data.Question.get(key='id', value=0))


class __Data:

    class __Question:
        @staticmethod
        def get(key=None, value=None):
            # if key is not None return the questions with key == value
            if key in ('id', 'vote_number', 'view_number'):
                condition = f"{key}={value}"
            else:
                condition = f"UPPER({key}) LIKE UPPER('%{value}%')"
            cursor = connection.get_cursor()
            query = """
                SELECT *
                FROM question
                {condition}
            """.format(
                condition=f"WHERE {condition}" if key else ""
            )
            cursor.execute(query)
            data = cursor.fetchall()
            connection.close_connection(cursor)
            return data[0] if key == 'id' else data

        @staticmethod
        def add(title, message, image, user_id):
            cursor = connection.get_cursor()
            cursor.execute("SELECT nextval('question_id_seq')")
            id = cursor.fetchall()[0]['nextval']
            query = """
                INSERT INTO question(id, submission_time, view_number, vote_number, title, message, image, user_id)
                VALUES ({id}, '{time}', 0, 0, '{title}', '{message}', '{image}', {user_id})
            """.format(
                id=id,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                title=title,
                message=message,
                image=f"question_{id}.{image}" if image else '',
                user_id=user_id
            )
            cursor.execute(query)
            query_for_question_count = f"""
                UPDATE "user"
                SET questions = questions + 1
                WHERE user_id = {user_id}
                """
            cursor.execute(query_for_question_count)
            connection.close_connection(cursor)
            return id

        @staticmethod
        def update(id: int, view=None, vote=None, title=None, message=None, image=None):
            cursor = connection.get_cursor()
            query = """
                UPDATE question
                SET {view}{vote}{title}{message}{image}
                WHERE id={id}
            """.format(
                id=id,
                view=f"view_number={view}{',' if vote != None or title or message or image else ''}" if view is not None else '',
                vote=f"vote_number={vote}{',' if title or message or image else ''}" if vote is not None else '',
                title=f"title='{title}'{',' if message or image else ''}" if title else '',
                message=f"message='{message}'{',' if image else ''}" if message else '',
                image=f"image='{image}'" if image else ''
            )
            cursor.execute(query)
            connection.close_connection(cursor)

        @staticmethod
        def delete(id: int, user_id):
            cursor = connection.get_cursor()
            query = """
                DELETE FROM question
                WHERE id={id}
            """.format(
                id=id
            )
            cursor.execute(query)
            query_for_question_count_delete = f"""
                UPDATE "user"
                SET questions = questions - 1
                WHERE user_id = {user_id}
            """
            cursor.execute(query_for_question_count_delete)
            connection.close_connection(cursor)

    class __Answer:
        @staticmethod
        def get(key=None, value=None):
            # if key is not None return the answers with key == value
            if key in ('id', 'vote_number', 'question_id'):
                condition = f"{key}={value}"
            else:
                condition = f"UPPER({key}) LIKE UPPER('%{value}%')"
            cursor = connection.get_cursor()
            query = """
                SELECT *
                FROM answer
                {condition}
            """.format(
                condition=f"WHERE {condition}" if key else ""
            )
            cursor.execute(query)
            data = cursor.fetchall()
            connection.close_connection(cursor)
            return data[0] if key == 'id' else data

        @staticmethod
        def add(question_id: int, message, image, user_id):
            cursor = connection.get_cursor()
            cursor.execute("SELECT nextval('answer_id_seq')")
            id = cursor.fetchall()[0]['nextval']
            query = """
                INSERT INTO answer(id, submission_time, vote_number, question_id, message, image, user_id)
                VALUES ({id}, '{time}', 0, {question}, '{message}', '{image}', '{user_id}')
            """.format(
                id=id,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                question=question_id,  # TODO
                message=message,
                image=f"answer_{id}.{image}" if image else '',
                user_id=user_id
            )
            cursor.execute(query)
            query_for_answer_count = f"""
                UPDATE "user"
                SET answers = answers + 1
                WHERE user_id = {user_id}
            """
            cursor.execute(query_for_answer_count)
            connection.close_connection(cursor)
            return id

        @staticmethod
        def update(id: int, vote=None, message=None, image=None):
            cursor = connection.get_cursor()
            query = """
                UPDATE answer
                SET {vote}{message}{image}
                WHERE id={id}
            """.format(
                id=id,
                vote=f"vote_number={vote}{',' if message or image else ''}" if vote is not None else '',
                message=f"message='{message}'{',' if image else ''}" if message else '',
                image=f"image='{image}'" if image else ''
            )
            cursor.execute(query)
            connection.close_connection(cursor)

        @staticmethod
        def delete(id: int, user_id):
            cursor = connection.get_cursor()
            query = """
                DELETE FROM answer
                WHERE id={id}
            """.format(
                id=id
            )
            cursor.execute(query)
            query_for_answer_count_delete = f"""
                UPDATE "user"
                SET answers = answers - 1
                WHERE user_id = {user_id}
            """
            cursor.execute(query_for_answer_count_delete)
            connection.close_connection(cursor)

    class __Comment:
        @staticmethod
        def get(key=None, value=None):
            if key in ('id', 'question_id', 'answer_id', 'edited_count'):
                condition = f"{key}={value}"
            else:
                condition = f"UPPER({key}) LIKE UPPER('%{value}%')"
            cursor = connection.get_cursor()
            query = """
                SELECT *
                FROM comment
                {condition}
            """.format(
                condition=f"WHERE {condition}" if key else ""
            )
            cursor.execute(query)
            data = cursor.fetchall()
            connection.close_connection(cursor)
            return data[0] if key == 'id' else data

        @staticmethod
        def add(message, user_id, question_id: int = None, answer_id: int = None):
            cursor = connection.get_cursor()
            cursor.execute("SELECT nextval('comment_id_seq')")
            id = cursor.fetchall()[0]['nextval']
            query = """
                INSERT INTO comment(id{id_for}, message, submission_time, edited_count, user_id)
                VALUES ({id}, {question}{answer}, '{message}', '{time}', 0, {user_id})
            """.format(
                id=id,
                id_for=f", {'question_id' if question_id != None else 'answer_id' if answer_id != None else ''}",
                question=question_id if question_id is not None else '',
                answer=answer_id if answer_id is not None else '',
                message=message,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_id=user_id
            )
            cursor.execute(query)
            query_for_comment_count = f"""
                UPDATE "user"
                SET comments = comments + 1
                WHERE user_id = {user_id}
            """
            cursor.execute(query_for_comment_count)
            connection.close_connection(cursor)
            return id

        @staticmethod
        def update(id: int, message=None, edited_count: int = None):
            cursor = connection.get_cursor()
            query = """
                UPDATE comment
                SET {message}{edited}
                WHERE id={id}
            """.format(
                id=id,
                message=f"message='{message}'{',' if edited_count != None else ''}" if message else '',
                edited=f"edited_count={edited_count}" if edited_count is not None else ''
            )
            cursor.execute(query)
            connection.close_connection(cursor)

        @staticmethod
        def delete(id: int, user_id):
            cursor = connection.get_cursor()
            query = """
                DELETE FROM comment
                WHERE id={id}
            """.format(
                id=id
            )
            cursor.execute(query)
            query_for_comment_count_delete = f"""
                UPDATE "user"
                SET comments = comments - 1
                WHERE user_id = {user_id}
            """
            cursor.execute(query_for_comment_count_delete)
            connection.close_connection(cursor)

    class __Tag:
        @staticmethod
        def get(question_id: int = None):
            cursor = connection.get_cursor()
            query = """
                SELECT {elements}
                FROM tag
                {condition}
            """.format(
                elements=f"{'id, name' if question_id != None else '*'}",
                condition=f"WHERE id IN (SELECT tag_id FROM question_tag WHERE question_id={question_id})" if question_id is not None else ''
            )
            cursor.execute(query)
            data = cursor.fetchall()
            connection.close_connection(cursor)
            return data

        @staticmethod
        def add(question_id: int, tag_id: int):
            try:
                cursor = connection.get_cursor()
                query = """
                    INSERT INTO question_tag(question_id, tag_id)
                    VALUES ({question}, {tag})
                """.format(
                    question=question_id,
                    tag=tag_id
                )
                cursor.execute(query)
                connection.close_connection(cursor)
            except IndexError:
                pass
            except KeyError:
                pass
            except ValueError:
                pass
            except IndentationError:
                pass

        @staticmethod
        def remove(question_id: int, tag_id: int):
            cursor = connection.get_cursor()
            query = """
                DELETE FROM question_tag
                WHERE question_id={question} AND tag_id={tag}
            """.format(
                question=question_id,
                tag=tag_id
            )
            cursor.execute(query)
            connection.close_connection(cursor)

        @staticmethod
        def new(name):
            cursor = connection.get_cursor()
            query = """
                INSERT INTO tag(name)
                VALUES ('{name}')
            """.format(
                name=name
            )
            cursor.execute(query)
            connection.close_connection(cursor)

    __question = __Question()
    __answer = __Answer()
    __comment = __Comment()
    __tag = __Tag()

    @property
    def Question(self): return self.__question

    @property
    def Answer(self): return self.__answer

    @property
    def Comment(self): return self.__comment

    @property
    def Tag(self): return self.__tag


Data = __Data()
