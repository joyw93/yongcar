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
        age = request.form['age']
        odo = int(request.form['odo'])
        fuel = request.form['fuel']
        color = request.form['color']
        price = Predict.price(lgbm, model, age, odo, fuel, color)
        return render_template('car/car_form.html',manufact=manufact, model=model, age=age, odo=odo, fuel=fuel, price=price)
    return render_template('car/car_form.html')





@bp.route('/info')
def info():
    model = request.args.get('model')
    age = request.args.get('age')
    odo = int(request.args.get('odo'))
    fuel = request.args.get('fuel')
    color = request.args.get('color')
    result = Predict.price(lgbm, model, age, odo, fuel, color)

    return render_template('car/car_info.html', result=result)




