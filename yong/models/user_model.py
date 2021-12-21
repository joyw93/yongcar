from flask_login import UserMixin
from yong.mysql import conn_mysqldb


class User(UserMixin):
    def __init__(self, user_id, user_name, user_email, user_pw):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_pw = user_pw


    def get_id(self):
        return str(self.user_id)


    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_table WHERE user_id = '" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_id=user[0], user_name=user[1], user_email=user[2], user_pw=user[3])
        return user


    @staticmethod
    def find(user_email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_table WHERE user_email = '" + \
              str(user_email) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_name=user[1], user_email=user[2], user_pw=user[3])
        return user


    @staticmethod
    def create(user_name, user_email, user_pw):
        user = User.find(user_email)
        if user is None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_table (user_name, user_email, user_pw) VALUES ('%s', '%s', '%s')" % (
                str(user_name), str(user_email), str(user_pw))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_email)
        else:
            return user