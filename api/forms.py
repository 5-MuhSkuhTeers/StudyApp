from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import TimeField


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(), EqualTo('password',message='Passwords Must Match')])
    submit = SubmitField('Sign Up')


class RequestForgotPasswordForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ForgotPasswordForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password',message='Passwords Must Match')
    ])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    status = StringField(label='Update status', validators=[DataRequired()])
    submit = SubmitField('Update Account')


class ChangePasswordForm(FlaskForm):
    current = PasswordField(label='Current Password', validators=[DataRequired()])
    new = PasswordField(label='New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new',message='Passwords Must Match')
    ])
    submit = SubmitField('Change Password')

class AddClassForm(FlaskForm):
    className = StringField(label='Class Name', validators=[DataRequired()])
    startTime = TimeField(label='Start Time', validators=[DataRequired()])
    endTime = TimeField(label='End Time', validators=[DataRequired()])
    M = BooleanField(label='Monday')
    T = BooleanField(label='Tuesday')
    W = BooleanField(label='Wednesday')
    Th = BooleanField(label='Thursday')
    F = BooleanField(label='Friday')
    submit = SubmitField('Add Class')