from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
import joblib
from ..config import BUCKET_PATH
import uuid
from yong.utils import Utils
from yong.models.car_model import Car
from yong.models.pagination_model import Pagination
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

bp = Blueprint('car', __name__, url_prefix='/car')
lgbm = joblib.load('lgbm_model.pkl')



@bp.route('/predict', methods=['GET','POST'])
def predict():
    
   
    if request.method =='POST':
        manufact = request.form['manufact']
        model = request.form['model']
        age = int(request.form['age'])
        odo = int(request.form['odo'].replace(',', ''))
        fuel = request.form['fuel']
        color = request.form['color']
        price = Utils.predict_price(lgbm, model, age, odo, fuel, color)
        
        return render_template('car/predict_car.html',manufact=manufact, model=model, age=age, odo=odo, fuel=fuel, price=price)
        

    return render_template('car/predict_car.html')


@bp.route('/list/', defaults={'current_page': 1})
@bp.route('/list/<int:current_page>', methods=['GET','POST'])
def _list(current_page):
    list_size = Car.get_size()
    page_size=9
    current_page_count = 3
    pagination = Pagination(list_size,page_size,current_page_count)

    page_count = pagination.page_count
    if current_page>page_count:
        current_page=page_count
    
    elif current_page<=0:
        current_page=1
    
    car_list = Car.get_page((current_page-1)*page_size,page_size)

    start_page = int((current_page-1)/current_page_count)*current_page_count+1
    if (page_count-start_page)<current_page_count:
        page_length = (page_count-start_page)+1
    else:
        page_length = current_page_count
    
    return render_template('car/car_list.html',car_list=car_list, start_page=start_page, page_length=page_length, current_page=current_page)




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

        
        if file and Utils.check_allowed_file(file.filename):
            img_uid = uuid.uuid4().hex 
            img_url = BUCKET_PATH + img_uid
                    
            Car.create(user_id,manufact, model,age,odo,fuel,color,price,comment,img_url)
            Utils.upload_img(img_uid, file) 
            
            return redirect(url_for('car._list'))       
        
        else: 
            flash('이미지 파일만 업로드 가능합니다.(jpg, jpeg, png)')
            
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