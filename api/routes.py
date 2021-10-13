from api import server, bcrypt
from api.forms import LoginForm, RegisterForm
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
