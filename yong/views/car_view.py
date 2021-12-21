from flask import Blueprint, render_template, request
import os
from flask import Blueprint, render_template, request, flash, url_for, redirect
import uuid
from yong.utils import Utils
from yong.models.car_predict_model import CarPredict
from yong.models.car_model import Car
from yong.models.pagination_model import Pagination
from yong.models.car_data_model import CarData
from flask_login import current_user, login_required
from yong.config import BUCKET_PATH
# BUCKET_PATH = os.environ['BUCKET_PATH']


bp = Blueprint('car', __name__, url_prefix='/car')
cardata = CarData.get_data()


@bp.route('/predict', methods=['GET','POST'])
def predict():
    if request.method =='POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        car = CarPredict(manufact,model,age,odo,fuel,color)                   
        price = Utils.predict_price(model, age, odo, fuel, color)        
        price_newcar = int(Utils.predict_price(model, 2021, 0, fuel, color)*1.1)
        price_1 = Utils.predict_price(model, age-1, odo, fuel, color)
        price_3 = Utils.predict_price(model, age-3, odo, fuel, color)
        price_5 = Utils.predict_price(model, age-5, odo, fuel, color)
        price_list = [price_newcar, price, price_1, price_3, price_5]
        mean_odo = int(cardata[cardata['age'] == age]['odo'].mean())
        try:
            mean_model_odo = int(cardata[(cardata['age'] == age) & (cardata['model'] == model)]['odo'].mean())
        except:
            mean_model_odo = mean_odo
        return render_template('car/predict_car.html', car=car, model=model, odo=odo, price_list=price_list, mean_odo=mean_odo, mean_model_odo=mean_model_odo)
    price_list=[0, 0, 0, 0, 0]
    return render_template('car/predict_car.html', price_list=price_list)


@bp.route('/predict/report/<model>', methods=['GET','POST'])
def report(model):
    cardata = CarData.get_data()
    price_age_list = []
    price_odo_list = []
    model_list = []
    models=cardata['model'].unique()
    for model_ in models:model_list.append(len(cardata[cardata['model']==model_])) 
    for age in range(2000,2022):price_age_list.append(Utils.predict_price(model,age,0,'가솔린','black'))
    for odo in range(0,160000,10000):price_odo_list.append(Utils.predict_price(model,2021,odo,'가솔린','black'))
    return render_template('car/report_car.html', model_list=model_list, model=model, price_age_list=price_age_list, price_odo_list=price_odo_list)    


@bp.route('/list/', defaults={'current_page': 1})
@bp.route('/list/<int:current_page>', methods=['GET','POST'])
def _list(current_page):
    try:
        Car.get_size()
    except:
        None
    list_size = Car.get_size()
    page_size = 9
    current_page_count = 3
    pagination = Pagination(list_size,page_size,current_page_count)
    page_count = pagination.page_count
    if current_page > page_count:
        current_page = page_count
    elif current_page <= 0:
        current_page = 1
    car_list = Car.get_page((current_page-1)*page_size,page_size)
    start_page = int((current_page-1)/current_page_count)*current_page_count+1
    if (page_count-start_page) < current_page_count:
        page_length = (page_count-start_page) + 1
    else:
        page_length = current_page_count
    return render_template('car/car_list.html',list_size=list_size, car_list=car_list, start_page=start_page, page_length=page_length, current_page=current_page)


@bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        price = int(request.form['price'].replace(',', ''))
        comment = request.form['comment']
        user_id = current_user.user_id
        file = request.files['file']
        predicted_price = Utils.predict_price( model, age, odo, fuel, color)
        if file and Utils.check_allowed_file(file.filename):
            img_uid = uuid.uuid4().hex 
            img_url = BUCKET_PATH + img_uid
            Car.create(user_id,manufact, model,age,odo,fuel,color,price,comment,img_url,predicted_price)
            Utils.upload_img(img_uid, file) 
            return redirect(url_for('car._list'))
        elif not file:
            flash('차량 사진을 선택하세요.')
            return render_template('car/add_car.html')
        elif not Utils.check_allowed_file(file.filename): 
            flash('이미지 파일만 업로드 가능합니다. (jpg, jpeg, png)')
            return render_template('car/add_car.html')
    return render_template('car/add_car.html')


@bp.route('/detail/<int:car_id>', methods=['GET','POST'])
def detail(car_id):
    car = Car.get(car_id)
    return render_template('car/car_detail.html',car=car)


@bp.route('/delete/<int:car_id>')
@login_required
def delete(car_id):
    car = Car.get(car_id)
    img_uid = car.get_img_url().replace(BUCKET_PATH, '')
    Utils.delete_img(img_uid)
    Car.delete(car_id)   
    return redirect(url_for('car._list'))