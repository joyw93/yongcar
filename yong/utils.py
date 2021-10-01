import pandas as pd
import numpy as np
import os
import boto3
from botocore.client import Config
import locale
locale.setlocale(locale.LC_ALL, '')
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
ACCESS_SECRET_KEY = os.environ['ACCESS_SECRET_KEY']
BUCKET_NAME = os.environ['BUCKET_NAME']

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
    def upload_img(img_uid,file): # f = 파일명
        key = 'myflask/images/'+img_uid
        # '로컬의 해당파일경로'+ 파일명 + 확장자
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(BUCKET_NAME).put_object(
            Key=key, Body=file, ContentType='image/jpg')