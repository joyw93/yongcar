from flask import Blueprint, render_template, request
from flask_login import current_user
from ..forms import QuestionForm
from yong.models.question_model import Question

bp = Blueprint('test', __name__, url_prefix='/')


