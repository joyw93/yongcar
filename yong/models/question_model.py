import pymysql.cursors
from yong.mysql import conn_mysqldb


class Question:

    def __init__(self, question_id, user_id, title, content):
        self.question_id = question_id
        self.user_id = user_id
        self.title = title
        self.content = content

    def get_id(self):
        return str(self.question_id)

    @staticmethod
    def create(user_id, title, content):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO question_table (user_id, title, content) VALUES ('%s', '%s', '%s')" % (
                str(user_id), str(title), str(content))
        db_cursor.execute(sql)
        mysql_db.commit()

    @staticmethod
    def get(question_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM question_table WHERE question_id = '" + str(question_id) + "'"
        db_cursor.execute(sql)
        question = db_cursor.fetchone()
        if not question:
            return None

        question = Question(question_id=question[0], user_id=question[1], title=question[2], content=question[3])
        return question


    @staticmethod
    def get_list():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT question_id, title, content, user_name 
                 FROM question_table q 
                 JOIN user_table u ON q.user_id = u.user_id 
                 ORDER BY question_id;"""
        db_cursor.execute(sql)
        question_list = db_cursor.fetchall()
        return question_list

    @staticmethod
    def delete(question_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = """DELETE FROM question_table WHERE question_id = '%s';""" % str(question_id)
        db_cursor.execute(sql)
        mysql_db.commit()

