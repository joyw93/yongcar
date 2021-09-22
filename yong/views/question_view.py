from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from ..forms import QuestionForm
from yong.models.question_model import Question
from yong.models.answer_model import Answer

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
        question_list = Question.get_list()

        return render_template('question/question_list.html', question_list=question_list)

    return render_template('question/add_question.html', form=form)


@bp.route('/')
def _list():
    question_list = Question.get_list()
    return render_template('question/question_list.html', question_list=question_list)


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
    return redirect(url_for('main.home'))

