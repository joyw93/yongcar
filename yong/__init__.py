from flask import Flask
from yong.models.user_model import User
from flask_login import LoginManager
from yong.config import SECRET_KEY
import os
# SECRET_KEY = os.environ['SECRET_KEY']

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 파일업로드용량 10MB로 제한
    app.config['IMG_FOLDER'] = os.path.join('static')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"로그인이 필요합니다."
    login_manager.init_app(app)

    from .views import main_view, auth_view, question_view, test_view, answer_view, car_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(test_view.bp)
    app.register_blueprint(answer_view.bp)
    app.register_blueprint(car_view.bp)

    from .utils import Utils
    app.jinja_env.filters['datetime'] = Utils.format_datetime
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    return app
