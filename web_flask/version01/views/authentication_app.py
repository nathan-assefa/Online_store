#/usr/bin/python3
""" app module """
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from os import getenv
from web_flask.version01.forms.forms import RegisterForm
from web_flask.version01.forms.forms import LoginForm
from models.user import User
from models import storage
from web_flask.version01.views import app_views
#from web_flask.version01.app import bcrypt, db



@app_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = storage.user_by_email(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard", form=form))
    return render_template("login.html", form=form)

@app_views.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app_views.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User()
        new_user.first_name=form.firstname.data
        new_user.last_name=form.lastname.data
        new_user.email=form.email.data
        new_user.password=hashed_password

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app_views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = LoginForm()

    return render_template("dashboard.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
