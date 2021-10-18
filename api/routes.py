from api import server, bcrypt
from api.forms import *
from flask import render_template, flash


@server.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("login.html",form=form)

@server.route("/create-account", methods=['GET','POST'])
def createAccount():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("account creation successful",'success')
    return render_template("createAccount.html",form = form)
#needs to change in order to be able to send the email 
@server.route("/request-reset-password", methods=['GET','POST'])
def requestforgotPassword():
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("requestResetPassword.html",form=form)
#also this
@server.route("/reset-password", methods=['GET','POST'])
def forgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("resetPassword.html",form=form)
@server.route("/acc_pg", methods=['GET','POST'])
def home():
    
    return render_template("account_page.html")
