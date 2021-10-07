import pandas as pd
from yong.mysql import conn_mysqldb


mysql_db = conn_mysqldb()
db_cursor = mysql_db.cursor()
sql = "SELECT * FROM car_table WHERE model = '" + str('쏘나타') + "'"
db_cursor.execute(sql)
answer = db_cursor.fetchone()

print(answer)