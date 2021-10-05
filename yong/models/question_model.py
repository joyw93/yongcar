from datetime import time

import pymysql.cursors
from yong.mysql import conn_mysqldb
from datetime import datetime


class Question:

    def __init__(self, question_id, user_id, title, content, time):
        self.question_id = question_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.time = time

    def get_id(self):
        return str(self.question_id)


    @staticmethod
    def get_size():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT COUNT(*) FROM question_table ;"
        db_cursor.execute(sql)
        question_size = db_cursor.fetchone()
        return question_size[0]

    @staticmethod
    def create(user_id, title, content):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO question_table (user_id, title, content, time) VALUES ('%s', '%s', '%s', '%s')" % (
                str(user_id), str(title), str(content), str(datetime.now()))
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

        question = Question(question_id=question[0], user_id=question[1], title=question[2], content=question[3], time=question[4])
        return question


    @staticmethod
    def get_list():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT question_id, title, content, user_name, time
                 FROM question_table q 
                 JOIN user_table u ON q.user_id = u.user_id 
                 ORDER BY question_id DESC
                 ;"""
        db_cursor.execute(sql)
        question_list = db_cursor.fetchall()
        return question_list

    @staticmethod
    def get_page(page,range):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT question_id, title, content, user_name, time
                 FROM question_table q 
                 JOIN user_table u ON q.user_id = u.user_id 
                 ORDER BY question_id DESC
                 LIMIT %s,%s ;""" % (str(page), str(range))
        db_cursor.execute(sql)
        question_list = db_cursor.fetchall()
        return question_list




    @staticmethod
    def delete(question_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM question_table WHERE question_id = '%s';" % str(question_id)
        db_cursor.execute(sql)
        mysql_db.commit()

    @staticmethod
    def modify(title, content, question_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()

        sql = """UPDATE question_table 
                 SET title='%s', content='%s' 
                 WHERE question_id = '%s';
                 """ % (str(title), str(content), str(question_id))
        db_cursor.execute(sql)
        mysql_db.commit()

