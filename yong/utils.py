import pandas as pd
import numpy as np
from .config import ACCESS_KEY_ID, ACCESS_SECRET_KEY, BUCKET_NAME
import boto3
from botocore.client import Config
import locale
locale.setlocale(locale.LC_ALL, '')


class Utils:

    @staticmethod
    def predict_price(ml_model, model, age, odo, fuel, color):
        data = pd.DataFrame({'model': [model],
                             'age': [age],
                             'odo': [odo],
                             'fuel': [fuel],
                             'color': [color]})

        data['model'] = data['model'].astype('category')
        data['fuel'] = data['fuel'].astype('category')
        data['color'] = data['color'].astype('category')
        price = int(np.expm1(ml_model.predict(data))[0])

        return price


    @staticmethod
    def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
        return value.strftime(fmt)


    @staticmethod
    def handle_upload_img(f): # f = 파일명
        data = open('C:/Users/joyongwon/Desktop/'+f+'.jpg', 'rb')
        # '로컬의 해당파일경로'+ 파일명 + 확장자
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(BUCKET_NAME).put_object(
            Key=f, Body=data, ContentType='image/jpg')