from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from ..forms import QuestionForm
from yong.models.question_model import Question
from yong.models.answer_model import Answer
from yong.models.pagination_model import Pagination


bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.user_id
        Question.create(user_id, title, content)
        return redirect(url_for('question._list'))
    return render_template('question/add_question.html', form=form)


@bp.route('/list/', defaults={'current_page': 1})
@bp.route('/list/<int:current_page>')
def _list(current_page):
    try:
        Question.get_size()
    except:
        None
    list_size = Question.get_size()
    page_size = 5
    current_page_count = 3
    pagination = Pagination(list_size,page_size,current_page_count)
    page_count = pagination.page_count
    if current_page > page_count:
        current_page = page_count
    elif current_page <= 0:
        current_page = 1
    question_list = Question.get_page((current_page-1)*page_size,page_size)
    #question_list = Question.get_list()
    start_page = int((current_page-1)/current_page_count)*current_page_count+1
    if (page_count-start_page) < current_page_count:
        page_length = (page_count-start_page) + 1
    else:
        page_length = current_page_count
    return render_template('question/question_list.html', question_list=question_list, start_page=start_page, page_length=page_length, current_page=current_page)


@bp.route('/<int:question_id>')
def detail(question_id):
    question = Question.get(question_id)
    answer_list = Answer.get_list(question_id)
    return render_template('question/question_detail.html', question=question, answer_list=answer_list)


@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form['title']
        content = request.form['content']
        Question.modify(title, content, question_id)
        return redirect(url_for('main.home'))
    return render_template('question/add_question.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    Question.delete(question_id)
    return redirect(url_for('question._list'))