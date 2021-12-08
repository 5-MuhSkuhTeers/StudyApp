from api import server, bcrypt, login_manager
from api.models import *
from api.forms import *
from flask import render_template, flash, redirect, get_flashed_messages, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from api.email import send_reset_email, setNotifications, send_break, send_sleep
from api.models import User


@server.route("/", methods=['GET', 'POST'])
@server.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    get_flashed_messages()
    form = LoginForm()
    if form.validate_on_submit():
        if User.find_by_email(form.email.data):
            user = User.find_by_email(form.email.data)
            if bcrypt.check_password_hash(user.password, form.password.data):
                print("Login")
                send_break(form.email.data)
                send_sleep(form.email.data)
                login_user(user)
                return redirect('home')
            else:
                flash("Incorrect password entered", 'danger')
                return redirect('login')
        else:
            flash("No account with such email exists", 'danger')
            return redirect('login')
    return render_template("login.html",form=form)


@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
            print("Create account")
            send_break(form.email.data)
            send_sleep(form.email.data)
            return redirect('login')
    return render_template("createAccount.html",form = form)
#needs to change in order to be able to send the email


@server.route("/request-reset-password", methods=['GET','POST'])
def requestforgotPassword():
    if current_user.is_authenticated:
        return redirect('account')
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.find_by_email(email):
            token = User.find_by_email(email).reset_token()
            send_reset_email(email, token)
        flash("If the email matches our records, you will receive further instructions", 'info')
        return redirect(url_for('login'))
    return render_template("requestResetPassword.html",form=form)
#also this


@server.route("/reset-password/<token>", methods=['GET','POST'])
def forgotPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    user = User.verify_token(token)
    if not user:
        flash("Your token has expired", 'danger')
        return redirect(url_for('requestforgotPassword'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash("Password changed successfully!",'success')
        return redirect(url_for('login'))
    return render_template("resetPassword.html",form=form)


@server.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    name = current_user.name
    status = current_user.status
    if form.validate_on_submit():
        user = User.find_by_id(current_user.id)
        user.status = form.status.data
        db.session.commit()
        current_user.status = form.status.data
        return redirect(url_for("account"))
    return render_template("account.html", form=form, name=name, status=status)


@server.route("/home", methods=['GET','POST'])
@login_required
def home():
    form = AddClassForm()
    form2 = AddTaskForm()
    name = current_user.name
    status = current_user.status
    # get user email
    user = User.find_by_id(current_user.id)
    classes = User.find_by_email(current_user.email).course_schedule()
    assignments = User.find_by_email(current_user.email).user_assignments()
    if form.validate_on_submit():
        day = f'{int(form.M.data)}{int(form.T.data)}{int(form.W.data)}{int(form.Th.data)}{int(form.F.data)}'
        id = current_user.id
        Course(user_id=id, course_num=form.className.data, day_of_week=day,
               start_time=form.startTime.data, end_time=form.endTime.data).save_to_db()
        return redirect(url_for('home'))
    if form2.validate_on_submit():
        email = current_user.email
        task_name = form2.taskName.data
        due_date = form2.dueDate.data
        due_time = form2.dueTime.data
        setNotifications(user=email,taskName=task_name,dueDate=due_date,dueTime=due_time)
        id = current_user.id
        dueDateTime = datetime.combine(due_date, due_time)
        Assignment(user_id=id, course=form2.className.data, name=task_name,
                  due_date=dueDateTime).save_to_db()
        print(User.find_by_email('conansum@buffalo.edu').user_assignments())
        return redirect(url_for('home'))
    return render_template("homeScreen.html", form=form, form2=form2, name=name, status=status, classes=classes, assignments=assignments)


@server.route("/change-password", methods=['GET','POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.find_by_id(current_user.id)
        if bcrypt.check_password_hash(user.password, form.current.data):
            user.password = bcrypt.generate_password_hash(form.new.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('account'))
        else:
            flash("Incorrect password entered", 'danger')
            return redirect(url_for('changePassword'))
    return render_template('changePassword.html', form=form)


@server.route("/account/delete", methods=['GET','POST'])
@login_required
def delete_account():
    if current_user.is_authenticated:
        user = User.find_by_id(current_user.id)
        user.delete_from_db()
        flash('Account deleted successfully', 'success')
    return redirect(url_for('login'))
