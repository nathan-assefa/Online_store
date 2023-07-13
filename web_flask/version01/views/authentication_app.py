#/usr/bin/python3
""" app module """
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from web_flask.version01.forms.forms import RegisterForm
from web_flask.version01.forms.forms import LoginForm
from models.user import User
#from web_flask.version01.models import User
from models import storage
from web_flask.version01.app import db, bcrypt
from flask import Blueprint


app_auth = Blueprint('app_auth', __name__, url_prefix='/gebeya_hub/version01')


@app_auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User()
        new_user.first_name=form.firstname.data
        new_user.last_name=form.lastname.data
        new_user.email=form.email.data
        new_user.password=hashed_password
        """
        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()
        """
        storage.new(new_user)
        storage.save()
        return redirect(url_for("app_auth.login"))

    return render_template("register.html", form=form)

@app_auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = storage.user_by_email(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("app_auth.dashboard", form=form))
    return render_template("login.html", form=form)

@app_auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("app_auth.login"))


@app_auth.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = LoginForm()

    return render_template("dashboard.html", form=form)
