from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField("이름",
                       validators=[DataRequired('이름을 입력하세요.'), Length(min=2, max=20, message='이름이 적절하지 않습니다.')])
    email = StringField("이메일",
                        validators=[DataRequired('메일주소를 입력하세요.'), Email('이메일 형식이 아닙니다.'), Length(max=50, message='이메일 주소가 너무 깁니다.')] )
    pw = PasswordField("비밀번호",
                       validators=[DataRequired('비밀번호를 입력하세요.'), Length(min=4, max=100, message='비밀번호는 최소 4글자 이상이어야 합니다.')])
    pw_confirm = PasswordField("비밀번호 확인",
                       validators=[DataRequired('확인용 비밀번호를 입력하세요.'), EqualTo("pw", message='비밀번호가 일치하지 않습니다.')])
    submit = SubmitField("가입")


class LoginForm(FlaskForm):

    email = StringField("이메일",
                        validators=[DataRequired('메일주소를 입력하세요.'), Email('이메일 형식이 아닙니다.')])
    pw = PasswordField("비밀번호",
                       validators=[DataRequired('비밀번호를 입력하세요.')])
    submit = SubmitField("로그인")


class QuestionForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    submit = SubmitField("제출")


