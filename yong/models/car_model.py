import pymysql.cursors
from yong.mysql import conn_mysqldb
from yong.utils import Utils


class Car:
    def __init__(self, car_id, user_id, manufact, model, age, odo, fuel, color, price, comment, img_url):
        self.car_id = car_id
        self.user_id = user_id
        self.manufact = manufact
        self.model = model
        self.age = age
        self.odo = odo
        self.fuel = fuel
        self.color = color
        self.price = price
        self.comment = comment
        self.img_url = img_url
        self.predicted_price = price = Utils.predict_price(model, age, odo, fuel, color)


    def get_id(self):
        return str(self.car_id)    


    def get_user_id(self):
        return str(self.user_id)       


    def get_img_url(self):
        return str(self.img_url)


    @staticmethod
    def get_size():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT COUNT(*) FROM car_table ;"
        db_cursor.execute(sql)
        car_size = db_cursor.fetchone()
        return car_size[0]


    @staticmethod
    def create(user_id, manufact, model, age, odo, fuel, color, price, comment, img_url, predicted_price):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = """INSERT INTO car_table (user_id, manufact, model, age, odo, fuel, color, price, comment, img_url, predicted_price)
                 VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                 % (str(user_id),str(manufact), str(model), str(age), str(odo), str(fuel), str(color), str(price), str(comment), str(img_url), str(predicted_price))
        db_cursor.execute(sql)
        mysql_db.commit()
       

    @staticmethod
    def get(car_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM car_table WHERE car_id = '" + str(car_id) + "'"
        db_cursor.execute(sql)
        car = db_cursor.fetchone()
        car = Car(car_id=car[0],
                  user_id=car[1],
                  manufact=car[2],
                  model=car[3],
                  age=car[4],
                  odo=car[5],
                  fuel=car[6],
                  color=car[7],
                  price=car[8],
                  comment=car[9],
                  img_url=car[10])
        return car


    @staticmethod
    def get_list():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT *
                 FROM car_table
                 ORDER BY car_id DESC;"""
        db_cursor.execute(sql)
        car_list = db_cursor.fetchall()
        return car_list


    @staticmethod
    def get_page(page,range):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT *
                 FROM car_table
                 ORDER BY car_id DESC
                 LIMIT %s,%s ;""" % (str(page), str(range))
        db_cursor.execute(sql)
        car_list = db_cursor.fetchall()
        return car_list


    @staticmethod
    def delete(car_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM car_table WHERE car_id = '%s';" % str(car_id)
        db_cursor.execute(sql)
        mysql_db.commit()