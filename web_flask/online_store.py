#!/usr/bin/python3
""" app module """


from models import storage
from models.product import Product
from models.category import Category
from models.user import User
from models.url import Url
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


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://{}:{}@{}/{}'.format(
        getenv('ONLINE_STORE_MYSQL_USER'),
        getenv('ONLINE_STORE_MYSQL_PWD'),
        getenv('ONLINE_STORE_MYSQL_HOST'),
        getenv('ONLINE_STORE_MYSQL_DB')
        )

app.config["SECRET_KEY"] = "thisidsupposedtobeasecretkey"
app.config['JWT_SECRET_KEY'] = 'thisissupposedtobeajwtsecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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

@app.teardown_appcontext
def close_db(exit):
    """This context function gives back the
    connection once request is done"""
    storage.close()

# Landing Page
@app.route('/', strict_slashes=False)
def landing_page():
    return render_template('landing_page.html')

# Home Page
@app.route('/shop', strict_slashes=False)
def online_shop():
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.urls:
            image = product.urls[0].link  # Select the first image
        else:
            image = None
        products_data.append({
            'name': product.name,
            'image': image,
            'description': product.description,
            'price': product.price,
            'id': product.id,
            'category_id': product.category.id
            })
    # Pass the data to the template
    return render_template('index.html', products=products_data)

# Single Products Page
@app.route('/item/<string:category_id>/<string:product_id>/<string:product_name>', strict_slashes=False)
def item(category_id, product_id, product_name):
    products = storage.all(Product)
    products_data = []
    related_products_data = []

    for product in products.values():
        if product.id == product_id:
            if product.urls:
                main_image = product.urls[0]
                images = product.urls
            products_data.append({
                'name': product.name,
                'main_image': main_image,
                'images': images,
                'description': product.description,
                'price': product.price,
                'id': product.id,
                'category_id': product.category.id
                })
            break
    for related_products in products.values():
        if related_products.category_id == category_id:
            if related_products.urls:
                image = related_products.urls[0].link
            else:
                image = None
            if not related_products.id == product_id:
                if related_products.name == product_name:
                    related_products_data.append({
                        'name': related_products.name,
                        'image': image,
                        'description': related_products.description,
                        'price': related_products.price,
                        'id': related_products.id,
                        'category_id': related_products.category.id
                        })

    # Pass the data to the template
    return render_template('product_item.html',
            products=products_data[0],
            related_products=related_products_data
            )

# Products in main catagories
@app.route('/items/<string:category_id>')
def category(category_id):
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.category_id == category_id:
            if product.urls:
                image = product.urls[0].link  # Select the first image
            else:
                image = None
        
                products_data.append({
                    'name': product.name,
                    'image': image,
                    'description': product.description,
                    'price': product.price,
                    'id': product.id,
                    'category_id': product.category.id
                    })
    # Pass the data to the template
    return render_template('index.html', products=products_data)

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
    app.run(host="0.0.0.0", port=5000, debug=True)
