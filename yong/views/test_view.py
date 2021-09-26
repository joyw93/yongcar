from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from botocore.client import Config
import boto3
import joblib

bp = Blueprint('test', __name__, url_prefix='/test')




# def handle_upload_img(f): # f = 파일명
#     data = open('C:/Users/joyongwon/Desktop/'+f+'.jpg', 'rb')
#     # '로컬의 해당파일경로'+ 파일명 + 확장자
#     s3 = boto3.resource(
#         's3',
#         aws_access_key_id=ACCESS_KEY_ID,
#         aws_secret_access_key=ACCESS_SECRET_KEY,
#         config=Config(signature_version='s3v4')
#     )
#     s3.Bucket(BUCKET_NAME).put_object(
#         Key=f, Body=data, ContentType='image/jpg')


# handle_upload_img('sample_image')

@bp.route('/form', methods=['GET', 'POST'])
def form():
    

    return render_template('test_form.html')


@bp.route('/result')
def result():

    

    return render_template('test_result.html')
