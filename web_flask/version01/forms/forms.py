# usr/bin/python3
""" Forms class defination """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import (
    InputRequired,
    Email,
    Length,
    ValidationError,
    EqualTo,
    Regexp,
)
from models import storage


class LoginForm(FlaskForm):
    email = StringField(
        "email",
        validators=[InputRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "password",
        validators=[InputRequired(), Length(min=8)],
        render_kw={"placeholder": "Password"},
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = storage.user_by_email(email.data)
        if not user:
            raise ValidationError("Don't have an account; Register instead")


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
    firstname = StringField(
        "firstname",
        validators=[InputRequired(), Length(min=4, max=15)],
        render_kw={"placeholder": "First Name"},
    )
    lastname = StringField(
        "lastname",
        validators=[InputRequired(), Length(min=4, max=15)],
        render_kw={"placeholder": "Last Name"},
    )
    email = StringField(
        "email",
        validators=[InputRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "password",
        validators=[
            InputRequired(),
            Length(min=8, max=12),
            Regexp(
                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$",
                message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.",
            ),
        ],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[InputRequired(), Length(min=8, max=12), EqualTo("password")],
        render_kw={"placeholder": "Confirm Password"},
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("Username already Exists")
