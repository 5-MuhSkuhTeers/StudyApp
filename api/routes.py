from api import server, bcrypt, login_manager
from api.models import *
from api.forms import *
from flask import render_template, flash, redirect, get_flashed_messages
from flask_login import login_user, login_required, current_user, logout_user


@server.route("/", methods=['GET', 'POST'])
@server.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('account')
    get_flashed_messages()
    form = LoginForm()
    if form.validate_on_submit():
        if User.find_by_email(form.email.data):
            user = User.find_by_email(form.email.data)
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('account')
            else:
                flash("Incorrect password entered", 'danger')
                return redirect('login')
        else:
            flash("No account with such email exists", 'danger')
            return redirect('login')
    return render_template("login.html",form=form)


@server.route("/create-account", methods=['GET','POST'])
def createAccount():
    if current_user.is_authenticated:
        return redirect('account')
    form = RegisterForm()
    if form.validate_on_submit():
        if User.find_by_email(form.email.data):
            flash("Account already exists","danger")
        else:
            user = User(email=form.email.data, name=form.name.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
            user.save_to_db()
            flash("Account creation successful",'success')
            return redirect('login')
    return render_template("createAccount.html",form = form)
#needs to change in order to be able to send the email


@server.route("/request-reset-password", methods=['GET','POST'])
def requestforgotPassword():
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("requestResetPassword.html",form=form)
#also this


@server.route("/reset-password/<token>", methods=['GET','POST'])
def forgotPassword(token):
    if current_user.is_authenticated:
        return redirect('account')
    user = User.verify_token(token)
    if not user:
        flash("Your token has expired", 'danger')
        return redirect('requestforgotPassword')
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash("Password updated successfully!",'success')
        return redirect('login')
    return render_template("resetPassword.html",form=form)


@server.route("/account", methods=['GET','POST'])
@login_required
def account():
    logout_user()
    return render_template("account.html")
