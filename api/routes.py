from api import app
from api.forms import LoginForm
from flask import render_template, flash

@app.route("/", methods=['GET','POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login successful",'success')
    return render_template("login.html",form=form)
