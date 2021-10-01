from api import server, bcrypt
from api.models import Users
from api.forms import LoginForm, RegisterForm
from flask import render_template, flash


@server.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("login.html",form=form)
