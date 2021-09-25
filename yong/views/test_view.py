from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from yong.models.predict_model import Predict

import joblib

bp = Blueprint('test', __name__, url_prefix='/test')

lgbm = joblib.load('model.pkl')


@bp.route('/form', methods=['GET', 'POST'])
def form():
    

    return render_template('test_form.html')


@bp.route('/result')
def result():

    model = request.args.get('model')
    age = request.args.get('age')
    odo = int(request.args.get('odo'))
    fuel = request.args.get('fuel')
    color = request.args.get('color')

    price = Predict.price(lgbm, model, age, odo, fuel, color)

    return render_template('test_result.html', price=price)
