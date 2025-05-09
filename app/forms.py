from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from email_validator import validate_email, EmailNotValidError
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        if not username.data.isalpha():
            raise ValidationError('Имя должно содержать только буквы.')
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Такое имя уже существует.')

    def validate_email(self, email):
        try:
            validate_email(email.data)  # проверка формата
        except EmailNotValidError:
            raise ValidationError('Некорректный формат почты.')

        # Проверка уникальности
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Такая почта уже используется.')

class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class EditForm(FlaskForm):
    username = StringField('Новое имя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Новая почта', validators=[DataRequired(), Email()])
    new_password = PasswordField('Новый пароль')  # опционально
    confirm_password = PasswordField('Подтвердите пароль', validators=[EqualTo('new_password', message='Пароли не совпадают')])
    submit = SubmitField('Сохранить')

    def validate_email(self, email):
        from flask_login import current_user
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Такая почта уже используется.')