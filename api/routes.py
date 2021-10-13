from api import app
from api.forms import LoginForm, RequestForgotPasswordForm, ForgotPasswordForm
from flask import render_template, flash

@app.route("/", methods=['GET','POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("login.html",form=form)

#needs to change in order to be able to send the email 
@app.route("/request-reset-password", methods=['GET','POST'])
def requestforgotPassword():
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("requestResetPassword.html",form=form)
#also this
@app.route("/reset-password", methods=['GET','POST'])
def forgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("resetPassword.html",form=form)
