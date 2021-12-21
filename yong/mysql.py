import pymysql
import os
#from yong.config import MYSQL_HOST, MYSQL_USER_ID, MYSQL_USER_PW
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER_ID = os.environ['MYSQL_USER_ID']
MYSQL_USER_PW = os.environ['MYSQL_USER_PW']


MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user=MYSQL_USER_ID,
    passwd=MYSQL_USER_PW,
    db='flask_db',
    charset='utf8'
)


def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN