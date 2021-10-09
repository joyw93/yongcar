import pymysql.cursors
from pandas import json_normalize
from yong.mysql import conn_mysqldb

class CarData:




    @staticmethod
    def get_data():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT *
                    FROM car_data
                                    ;""" 
        db_cursor.execute(sql)
        car_list = db_cursor.fetchall()
            
        df = json_normalize(car_list)
        return df