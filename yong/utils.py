import pandas as pd
import numpy as np
import os
from yong.config import ACCESS_KEY_ID, ACCESS_SECRET_KEY, BUCKET_NAME
import boto3
import joblib
from botocore.client import Config
import locale
locale.setlocale(locale.LC_ALL, '')
# ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
# ACCESS_SECRET_KEY = os.environ['ACCESS_SECRET_KEY']
# BUCKET_NAME = os.environ['BUCKET_NAME']



class Utils:

    @staticmethod
    def predict_price(model, age, odo, fuel, color):
        lgbm = joblib.load('lgbm_model.pkl')
        data = pd.DataFrame({'model': [model],
                             'age': [age],
                             'odo': [odo],
                             'fuel': [fuel],
                             'color': [color]})

        data['model'] = data['model'].astype('category')
        data['fuel'] = data['fuel'].astype('category')
        data['color'] = data['color'].astype('category')
        price = int(np.expm1(lgbm.predict(data))[0])

        return price


    @staticmethod
    def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
        return value.strftime(fmt)


    @staticmethod
    def upload_img(img_uid, file): 
        key = 'myflask/images/'+img_uid     
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(BUCKET_NAME).put_object(
            Key=key, Body=file, ContentType='image/jpg')

    @staticmethod
    def delete_img(img_uid):
        key = 'myflask/images/'+img_uid
        s3 = boto3.client('s3',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=ACCESS_SECRET_KEY,
                        config=Config(signature_version='s3v4'))
        s3.delete_object(Bucket=BUCKET_NAME, Key=key)



    @staticmethod
    def check_allowed_file(filename):
        ALLOWED_EXTENSIONS = set(['JPG','png', 'jpg', 'jpeg'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


    # @staticmethod
    # def create_dataset(URI,page,manufact,model,fuel):
    #   count=0
    #   columns = ['name','age','odo','price']
    #   url=''
    #   name=[]
    #   age=[]
    #   odo=[]
    #   price=[]
    #   df=pd.DataFrame()
    
    #   features = [name, age, odo, price]
    #   name_selector = '#content > div.common-sub-content.fix-content > div > div.searchArea > div.searchArea__carList > div.__used-car-list > div.cs-list02.cs-list02--ratio.small-tp.generalRegist > div.list-in > div > div.con > div > a > strong.tit'
    #   age_selector = '#content > div.common-sub-content.fix-content > div > div.searchArea > div.searchArea__carList > div.__used-car-list > div.cs-list02.cs-list02--ratio.small-tp.generalRegist > div.list-in > div > div.con > div > a > div > div.first'
    #   odo_selector = '#content > div.common-sub-content.fix-content > div > div.searchArea > div.searchArea__carList > div.__used-car-list > div.cs-list02.cs-list02--ratio.small-tp.generalRegist > div.list-in > div > div.con > div > a > div > div.data-in > span:nth-child(1)'
    #   price_selector = '#content > div.common-sub-content.fix-content > div > div.searchArea > div.searchArea__carList > div.__used-car-list > div.cs-list02.cs-list02--ratio.small-tp.generalRegist > div.list-in > div > div.con > div > a > strong.pay'

    #   selectors = [name_selector, age_selector, odo_selector, price_selector]
    
    #   for i in range(page):
    #       wd = webdriver.Chrome('chromedriver', options=chrome_options)
    #       time.sleep(0.1)


    #       url = URI+'countryOrder=1&page={0}'.format(i+1)+'&sort=-orderDate&makerCode='+manufact+'&classCode='+model+'&gas='+fuel
    #       print('{0}페이지 완료'.format(i))
    #       wd.get(url)
    #       for selector,feature in zip(selectors,features):
    #         for label in wd.find_elements_by_css_selector(selector):       
    #             feature.append(label.text)
            
            
    #       for i in range(len(features)):
    #         features[i] = pd.DataFrame(features[i])
    #         df = pd.concat([df,features[i]],axis=1)

    #         df.columns=columns
    #         df['manufacturer']=manufact
    #         df['model']=model
    #         df['fuel']=fuel
    #         df['color']=color

    #         fname = manufact+model+fuel+'.csv'

    #         df.to_csv(fname, index=False, encoding='cp949')
    #         df.to_csv('/content/drive/MyDrive/'+fname, index=False, encoding='cp949')
            
    #         return df
    