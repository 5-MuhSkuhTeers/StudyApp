from api import app
from api.forms import LoginForm, accountCreationForm
from flask import render_template, flash

@app.route("/", methods=['GET','POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("login.html",form=form)

@app.route("/create-account", methods=['GET','POST'])
def home():
    form = accountCreationForm()
    if form.validate_on_submit():
        flash("account creation successful",'success')
    return render_template("createAccount.html",form = form)
