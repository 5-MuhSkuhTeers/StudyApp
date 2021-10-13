from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RequestForgotPasswordForm (FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ForgotPasswordForm (FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password',message='Passwords Must Match')
    ])
    submit = SubmitField('Login')

