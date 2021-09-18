from flask import Blueprint, render_template, request
from flask_login import current_user
from ..forms import QuestionForm
from yong.models.question_model import Question

bp = Blueprint('test', __name__, url_prefix='/')


@bp.route('/qtest')
def test1():
    question_list = Question.get_list()
    return render_template('test.html', question_list=question_list)