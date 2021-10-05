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
    
    return render_template('test_form.html', question_list=question_list, page_count=page_count)


@bp.route('/result/<int:page>')
def result(page):
    pagination = Pagination()
    list_size = 5
    question_size = Question.get_size()
    page_count = math.ceil(question_size/list_size)
    question_list = Question.get_page(page*list_size,list_size)    
    
    if (page%3 == 0) & (page>0):
        pagination.temp = pagination.temp+3
        return render_template('test_result.html',question_list=question_list, page_count=page_count, page=page, temp=pagination.temp)
   
    
    return render_template('test_result.html',question_list=question_list, page_count=page_count, page=page, temp=pagination.temp)
