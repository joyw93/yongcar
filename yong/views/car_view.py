from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
import joblib
from ..config import BUCKET_PATH
import uuid
from yong.utils import Utils
from yong.models.car_model import Car
from yong.models.pagination_model import Pagination
from yong.models.car_data_model import CarData
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
        
        price_newcar =int(Utils.predict_price(lgbm, model, 2021, 0, fuel, color)*1.1)
        price_now = Utils.predict_price(lgbm, model, age, odo, fuel, color)
        price_1 = Utils.predict_price(lgbm, model, age-1, odo, fuel, color)
        price_3 = Utils.predict_price(lgbm, model, age-3, odo, fuel, color)
        price_5 = Utils.predict_price(lgbm, model, age-5, odo, fuel, color)
        price_list=[price_newcar, price_now, price_1, price_3, price_5]
        return render_template('car/predict_car.html',manufact=manufact, model=model, age=age, odo=odo, fuel=fuel, price=price, price_list=price_list)
        
    price_list=[0,0,0,0,0]
    return render_template('car/predict_car.html',price_list=price_list)


@bp.route('/predict/report/<model>', methods=['GET','POST'])
def report(model):
    
    df = CarData.get_data()
    # 현대
    avante = len(df[df['model']=='아반떼'])
    sonata = len(df[df['model']=='쏘나타'])
    grandeur = len(df[df['model']=='그랜저'])

    # 제네시스
    g70 = len(df[df['model']=='G70'])
    g80 = len(df[df['model']=='G80'])

    # 기아
    k3 = len(df[df['model']=='K3'])
    k5 = len(df[df['model']=='K5'])
    k7 = len(df[df['model']=='K7'])

    # 르노삼성
    sm3 = len(df[df['model']=='SM3'])
    sm5 = len(df[df['model']=='SM5'])
    sm6 = len(df[df['model']=='SM6'])
    sm7 = len(df[df['model']=='SM7'])

    # 쌍용
    tiboli = len(df[df['model']=='티볼리'])
    corando = len(df[df['model']=='코란도'])

    # GM대우
    cruse = len(df[df['model']=='크루즈'])
    malibu = len(df[df['model']=='말리부'])

    # 벤츠
    c_class = len(df[df['model']=='C클래스'])
    e_class = len(df[df['model']=='E클래스'])
    s_class = len(df[df['model']=='S클래스'])

    # BMW
    series_3 = len(df[df['model']=='3시리즈'])
    series_5 = len(df[df['model']=='5시리즈'])
    series_7 = len(df[df['model']=='7시리즈'])

    # 아우디
    a4 = len(df[df['model']=='A4'])
    a6 = len(df[df['model']=='A6'])
    a7 = len(df[df['model']=='A7'])

    # 폭스바겐
    golf = len(df[df['model']=='골프'])
    tiguan = len(df[df['model']=='티구안'])
    passat = len(df[df['model']=='파사트'])  

    model_list = [avante,sonata,grandeur,g70,g80,k3,k5,k7,sm3,sm5,sm6,sm7,tiboli,corando,cruse,malibu,c_class,e_class,s_class,series_3,series_5,series_7,a4,a6,a7,golf,tiguan,passat]    
    

    price_2000 = Utils.predict_price(lgbm, model, 2000, 0, '가솔린', 'black')
    price_2001 = Utils.predict_price(lgbm, model, 2001, 0, '가솔린', 'black')
    price_2002 = Utils.predict_price(lgbm, model, 2002, 0, '가솔린', 'black')
    price_2003 = Utils.predict_price(lgbm, model, 2003, 0, '가솔린', 'black')
    price_2004 = Utils.predict_price(lgbm, model, 2004, 0, '가솔린', 'black')
    price_2005 = Utils.predict_price(lgbm, model, 2005, 0, '가솔린', 'black')
    price_2006 = Utils.predict_price(lgbm, model, 2006, 0, '가솔린', 'black')
    price_2007 = Utils.predict_price(lgbm, model, 2007, 0, '가솔린', 'black')
    price_2008 = Utils.predict_price(lgbm, model, 2008, 0, '가솔린', 'black')
    price_2009 = Utils.predict_price(lgbm, model, 2009, 0, '가솔린', 'black')
    price_2010 = Utils.predict_price(lgbm, model, 2010, 0, '가솔린', 'black')
    price_2011 = Utils.predict_price(lgbm, model, 2011, 0, '가솔린', 'black')
    price_2012 = Utils.predict_price(lgbm, model, 2012, 0, '가솔린', 'black')
    price_2013 = Utils.predict_price(lgbm, model, 2013, 0, '가솔린', 'black')
    price_2014 = Utils.predict_price(lgbm, model, 2014, 0, '가솔린', 'black')
    price_2015 = Utils.predict_price(lgbm, model, 2015, 0, '가솔린', 'black')
    price_2016 = Utils.predict_price(lgbm, model, 2016, 0, '가솔린', 'black')
    price_2017 = Utils.predict_price(lgbm, model, 2017, 0, '가솔린', 'black')
    price_2018 = Utils.predict_price(lgbm, model, 2018, 0, '가솔린', 'black')
    price_2019 = Utils.predict_price(lgbm, model, 2019, 0, '가솔린', 'black')
    price_2020 = Utils.predict_price(lgbm, model, 2020, 0, '가솔린', 'black')
    price_2021 = Utils.predict_price(lgbm, model, 2021, 0, '가솔린', 'black')

    price_age_list = [price_2000,
                      price_2001,
                      price_2002,
                      price_2003,
                      price_2004,
                      price_2005,
                      price_2006,
                      price_2007,
                      price_2008,
                      price_2009,
                      price_2010,
                      price_2011,
                      price_2012,
                      price_2013,
                      price_2014,
                      price_2015,
                      price_2016,
                      price_2017,
                      price_2018,
                      price_2019,
                      price_2020,
                      price_2021]


    price_0km = Utils.predict_price(lgbm, model, 2021, 0, '가솔린', 'black')
    price_10000km = Utils.predict_price(lgbm, model, 2021, 10000, '가솔린', 'black')
    price_20000km = Utils.predict_price(lgbm, model, 2021, 20000, '가솔린', 'black')
    price_30000km = Utils.predict_price(lgbm, model, 2021, 30000, '가솔린', 'black')
    price_40000km = Utils.predict_price(lgbm, model, 2021, 40000, '가솔린', 'black')
    price_50000km = Utils.predict_price(lgbm, model, 2021, 50000, '가솔린', 'black')
    price_60000km = Utils.predict_price(lgbm, model, 2021, 60000, '가솔린', 'black')
    price_70000km = Utils.predict_price(lgbm, model, 2021, 70000, '가솔린', 'black')
    price_80000km = Utils.predict_price(lgbm, model, 2021, 80000, '가솔린', 'black')
    price_90000km = Utils.predict_price(lgbm, model, 2021, 90000, '가솔린', 'black')
    price_100000km = Utils.predict_price(lgbm, model, 2021, 100000, '가솔린', 'black')
    price_110000km = Utils.predict_price(lgbm, model, 2021, 110000, '가솔린', 'black')
    price_120000km = Utils.predict_price(lgbm, model, 2021, 120000, '가솔린', 'black')
    price_130000km = Utils.predict_price(lgbm, model, 2021, 130000, '가솔린', 'black')
    price_140000km = Utils.predict_price(lgbm, model, 2021, 140000, '가솔린', 'black')
    price_150000km = Utils.predict_price(lgbm, model, 2021, 150000, '가솔린', 'black')

    price_odo_list = [price_0km,
                      price_10000km,
                      price_20000km,
                      price_30000km,
                      price_40000km,
                      price_50000km,
                      price_60000km,
                      price_70000km,
                      price_80000km,
                      price_90000km,
                      price_100000km,
                      price_110000km,
                      price_120000km,
                      price_130000km,
                      price_140000km,
                      price_150000km]


    return render_template('car/report_car.html', df=df, model_list=model_list, model=model, price_age_list=price_age_list, price_odo_list=price_odo_list)    




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
    
    return render_template('car/car_list.html',list_size=list_size, car_list=car_list, start_page=start_page, page_length=page_length, current_page=current_page)




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