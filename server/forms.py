from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, ValidationError
from wtforms.validators import data_required, email, equal_to
from server.models import User


class ArticleForm(FlaskForm):
    title = StringField('Title:', validators=[data_required()])
    text = TextAreaField('Text:', validators=[data_required()])

    def validate_title(self, title):
        if len(title.data) > 50:
            raise ValidationError('Please use a maximum of 50 characters.')

    def validate_text(self, text):
        if len(text.data) > 400:
            raise ValidationError('Please use a maximum of 400 characters.')


class ContactForm(FlaskForm):
    email = StringField('Email:', validators=[data_required(), email()])
    message = TextAreaField('Message')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    email = StringField('Email', validators=[data_required(), email()])
    password = PasswordField('Password', validators=[data_required()])
    password2 = PasswordField('Repeat Password', validators=[data_required(), equal_to('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
