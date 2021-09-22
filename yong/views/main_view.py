from flask import Blueprint, render_template
from yong.models.question_model import Question

bp = Blueprint('main', __name__, url_prefix='/')


# @bp.route('/')
# def home():
#     question_list = Question.get_list()
#     return render_template('question/question_list.html', question_list=question_list)

@bp.route('/')
def home():
    return render_template('main.html')
