from flask import Blueprint, render_template, request
import joblib
from yong.models.predict_model import Predict

bp = Blueprint('car', __name__, url_prefix='/car')
lgbm = joblib.load('model.pkl')



@bp.route('/form', methods=['GET','POST'])
def form():
    
    if request.method =='POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        price = Predict.price(lgbm, model, age, odo, fuel, color)
        odo = format(odo, ',')
        price = format(price, ',')
        return render_template('car/car_form.html',manufact=manufact, model=model, age=age, odo=odo, fuel=fuel, price=price)
        

    return render_template('car/car_form.html')





