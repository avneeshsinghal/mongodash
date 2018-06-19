from app import app, lm
from flask import request, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .forms import RegisterForm
from .user import User
import datetime
from app import sock

from datetime import timedelta
from flask import session


@app.before_request
def make_session_permanent():

    """
    make session for 24 Hr
    :return:
    """
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1440)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('write'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:          # if user already logged then --> write.html
        return redirect(url_for('write'))
    form = LoginForm()                         # user LoginForm
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"user_name": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['user_name'])
            login_user(user_obj)
            return redirect(url_for("write"))
        return render_template("login.html", form=form, title="login", error1="user name or password is incorrect")
    return render_template('login.html', title='login', form=form)


@app.route('/logout')                          # if logout then --> login.html
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/write')
@login_required
def write():
    ip = sock.get_ip_address()
    return render_template('textbox.html',ip=ip)   # send host to textbox.html


@login_required
@app.route('/register', methods=['GET', 'POST'])
def register():
    ip = sock.get_ip_address()
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"user_name": form.username.data})
        if user is None:
            register_username = form.username.data
            register_password = form.password.data
            date_time = datetime.datetime.now()
            current_date_time = str(date_time)
            app.config['USERS_COLLECTION'].insert(
                {"user_name": register_username, "password": register_password, "added_by": current_user.username ,"added_time" : current_date_time})
            return render_template('textbox.html',ip=ip)
        else:
            return render_template("register.html", form=form, title="login", error1="user already exist")
    return render_template('register.html', title='login', form=form)


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"user_name": username})
    if not u:
        return None
    return User(u['user_name'])


