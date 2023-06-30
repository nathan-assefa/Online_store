#/usr/bin/python3
""" app module """
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import InputRequired, Email, Length, ValidationError, EqualTo, Regexp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from os import getenv
from models.user import User
from models import storage


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://{}:{}@{}/{}'.format(
        getenv('ONLINE_STORE_MYSQL_USER'),
        getenv('ONLINE_STORE_MYSQL_PWD'),
        getenv('ONLINE_STORE_MYSQL_HOST'),
        getenv('ONLINE_STORE_MYSQL_DB')
        )

app.config["SECRET_KEY"] = "thisidsupposedtobeasecretkey"
app.config['JWT_SECRET_KEY'] = 'thisissupposedtobeajwtsecretkey'

#db.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#jwt = JWTManager(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    user = storage.user_by_id(user_id)
    return user

class LoginForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("password", validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = storage.user_by_email(email.data)
        if not user:
            raise ValidationError(
                    "Don't have an account; Register instead")

"""
    def validate_password(self):
        user = storage.user_by_email(email.data)
        if user:
            #if not bcrypt.check_password_hash(password = user_email.password, password.data):
            hashed_entered_password = bcrypt.hashpw(password.data.encode('utf-8'), user_email.password)
            #if not bcrypt.check_password_hash(user_email.password, password):
            if not hashed_entered_password == user.password:
                raise ValidationError(
                        "Unauthorized access")
"""


class RegisterForm(FlaskForm):
    firstname = StringField("firstname", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "First Name"})
    lastname = StringField("lastname", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Last Name"})
    email = StringField("email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    #username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField(
            "password",
            validators=[
                InputRequired(),
                Length(min=8, max=12),
                Regexp(
                    regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$",
                    message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
                    )
                ],
            render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("confirm_password", validators=[InputRequired(), Length(min=8, max=12), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    remember = BooleanField("Remember me")
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(
                username=username.data).first()
        if existing_username:
            raise ValidationError(
                    "Username already Exists")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = storage.user_by_email(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard", form=form))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
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

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = LoginForm()

    return render_template("dashboard.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', debug=True)
