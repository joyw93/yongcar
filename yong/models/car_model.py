import pymysql.cursors
from yong.mysql import conn_mysqldb


class Car:

    def __init__(self,model, age, odo, fuel, color):
        self.model = model
        self.age = age
        self.odo = odo
        self.fuel = fuel
        self.color = color

   





