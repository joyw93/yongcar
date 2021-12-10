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



@bp.route('/', methods=['GET', 'POST'])
def test():
    

    return render_template('test_form.html')


    





    

    
    
    return render_template('test_result.html')
