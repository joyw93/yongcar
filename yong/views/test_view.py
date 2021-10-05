from flask import Blueprint, render_template, request
from yong.models.question_model import Question
from yong.models.pagination_model import Pagination
import math
bp = Blueprint('test', __name__, url_prefix='/test')





@bp.route('/form', methods=['GET', 'POST'])
def form():
    
    
    list_size = 5
    question_size = Question.get_size()
    page_count = math.ceil(question_size/list_size)
    

    question_list = Question.get_page(0,5)
    
    return render_template('test_result.html', question_list=question_list, page=page_count)


@bp.route('/result/<page>')
def result(page):

        
    return page
   
    
    return render_template('test_result.html')
