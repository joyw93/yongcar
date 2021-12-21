import pymysql.cursors
from yong.mysql import conn_mysqldb


class Answer:
    def __init__(self,answer_id, user_id, question_id, content):
        self.answer_id = answer_id
        self.user_id = user_id
        self.question_id = question_id
        self.content = content


    def get_id(self):
        return str(self.answer_id)


    @staticmethod
    def create(user_id, question_id, content):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO answer_table (user_id, question_id, content) VALUES ('%s','%s', '%s')" % (
                str(user_id), str(question_id), str(content))
        db_cursor.execute(sql)
        mysql_db.commit()
        

    @staticmethod
    def get(answer_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM answer_table WHERE answer_id = '" + str(answer_id) + "'"
        db_cursor.execute(sql)
        answer = db_cursor.fetchone()
        if not answer:
            return None
        answer = Answer(answer_id=answer[0], user_id=answer[1], question_id=answer[2], content=answer[3])
        return answer


    @staticmethod
    def get_list(question_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT content, user_name, u.user_id, answer_id
                 FROM answer_table a
                 JOIN user_table u
                 ON a.user_id = u.user_id
                 WHERE question_id = '%s';""" % str(question_id)
        db_cursor.execute(sql)
        answer_list = db_cursor.fetchall()
        return answer_list


    @staticmethod
    def delete(answer_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM answer_table WHERE answer_id = '%s';" % str(answer_id)
        db_cursor.execute(sql)
        mysql_db.commit()