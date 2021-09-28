from flask import Blueprint, render_template, request, jsonify
import joblib
from yong.utils import Utils
from yong.models.car_model import Car

bp = Blueprint('car', __name__, url_prefix='/car')
lgbm = joblib.load('model.pkl')



@bp.route('/predict', methods=['GET','POST'])
def predict():
    
    # 리팩토링 필요 -> class로 구현
    if request.method =='POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        price = Utils.predict_price(lgbm, model, age, odo, fuel, color)
        odo = format(odo, ',')
        price = format(price, ',')
        return render_template('car/predict_car.html',manufact=manufact, model=model, age=age, odo=odo, fuel=fuel, price=price)
        

    return render_template('car/predict_car.html')




@bp.route('/list', methods=['GET','POST'])
def _list():
    return render_template('car/car_list.html')




@bp.route('/create', methods=['GET','POST'])
def create():
    if request.method =='POST':
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']

        car = Car(model, age, odo, fuel, color)
        return render_template('car/add_car.html',car=car)       
    return render_template('car/add_car.html')





@bp.route('/create/register', methods=['GET','POST'])
def register():
        
    return render_template('car/car_list.html')