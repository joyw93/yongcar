import pandas as pd
import numpy as np
from .config import ACCESS_KEY_ID, ACCESS_SECRET_KEY, BUCKET_NAME
import boto3
import joblib
from botocore.client import Config
import locale
locale.setlocale(locale.LC_ALL, '')



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