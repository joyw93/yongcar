from flask import Blueprint, render_template, request, jsonify
from yong.models.question_model import Question
from yong.models.pagination_model import Pagination
import math
import pandas as pd
import json
from pandas import json_normalize
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from lightgbm import LGBMRegressor
import pymysql.cursors
from yong.mysql import conn_mysqldb
import pandas as pd


bp = Blueprint('test', __name__, url_prefix='/test')



@bp.route('/form', methods=['GET', 'POST'])
def form():
    
    
    
    num = 5
    text = 'test'
    manufact='제네시스'
    model='G80'
    price_list = [500,400,300,200,100,0]

    return render_template('test_form.html' ,manufact=manufact, model=model, price_list=price_list)


@bp.route('/result')
def result():

    mysql_db = conn_mysqldb()
    db_cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
    sql = """SELECT *
             FROM car_data
                            ;""" 
    db_cursor.execute(sql)
    car_list = db_cursor.fetchall()
       
    df = json_normalize(car_list)
    





    

    
    
    return render_template('test_result.html')
