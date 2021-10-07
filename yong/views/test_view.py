from flask import Blueprint, render_template, request
from yong.models.question_model import Question
from yong.models.pagination_model import Pagination
import math
bp = Blueprint('test', __name__, url_prefix='/test')





@bp.route('/form', methods=['GET', 'POST'])
def form():
    
    
    
    
    return render_template('test_form.html')


@bp.route('/result')
def result():
   
    
    return render_template('test_result.html')
