from flask import Flask
from yong.models.user_model import User
from flask_login import LoginManager
from yong.key import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = key.SECRET_KEY
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"로그인이 필요합니다."
    login_manager.init_app(app)
    from .views import main_view, auth_view, question_view, test_view, answer_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(test_view.bp)
    app.register_blueprint(answer_view.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
