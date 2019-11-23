# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from app.texts import Texts

class LoginForm(FlaskForm):
    username = StringField(Texts.user, validators=[DataRequired()])
    password = PasswordField(Texts.password, validators=[DataRequired()])
    submit = SubmitField(Texts.login)        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Auth_error')
    def validate_password(self,password):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError('Auth_error')

class RegisterForm(FlaskForm):
    username = StringField(Texts.user, validators=[DataRequired()])
    email = StringField(Texts.email, validators=[DataRequired(),Email()])
    password = PasswordField(Texts.password, validators=[DataRequired()])
    submit = SubmitField(Texts.register)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(Texts.user_exists)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(Texts.email_exists)