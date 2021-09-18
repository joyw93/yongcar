from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from yong.models.answer_model import Answer
from yong.models.question_model import Question
bp = Blueprint('answer', __name__, url_prefix='/')


@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):

    content = request.form['content']
    user_id = current_user.user_id
    answer = Answer.create(user_id, question_id, content)
    return redirect(url_for('question.detail', question_id=answer.question_id))


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.get(answer_id)
    Answer.delete(answer_id)
    return redirect(url_for('question.detail', question_id=answer.question_id))

