from flask import Blueprint, render_template, request, jsonify
import joblib
from ..config import BUCKET_PATH
import uuid
from yong.utils import Utils
from yong.models.car_model import Car
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

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
    car_list = Car.get_list()
    return render_template('car/car_list.html',car_list=car_list)




@bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method =='POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        price =int(request.form['price'].replace(',', ''))
        comment = request.form['comment']
        user_id = current_user.user_id
        file = request.files['file']

        img_uid = uuid.uuid4().hex
        img_url = BUCKET_PATH + img_uid
        Utils.upload_img(img_uid, file)
        
        Car.create(user_id,manufact, model,age,odo,fuel,color,price,comment,img_url)
        car_list = Car.get_list()

        return render_template('car/car_list.html',car_list=car_list)       
    return render_template('car/add_car.html')



@bp.route('/detail/<int:car_id>', methods=['GET','POST'])
def detail(car_id):
    car = Car.get(car_id)
    return render_template('car/car_detail.html',car=car)