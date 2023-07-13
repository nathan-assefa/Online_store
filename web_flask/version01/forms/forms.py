# usr/bin/python3
""" Forms class defination """
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    validators
)
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
                regex=(
                    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
                    r"(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
                ),
                message="Password must contain at least one" +
                        " lowercase letter, one uppercase letter," +
                        " one digit, and one special character.",
                ),
        ],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            InputRequired(),
            Length(min=8, max=12),
            EqualTo("password")
        ],
        render_kw={"placeholder": "Confirm Password"},
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Register")

    def validate_username(self, username):
        _username = User.query.filter_by(username=username.data).first()
        if _username:
            raise ValidationError("Username already Exists")
