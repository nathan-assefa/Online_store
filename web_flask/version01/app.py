#!/usr/bin/python3
""" Flask Application """
from os import getenv
from models import storage
from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS


bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://{}:{}@{}/{}".format(
        getenv("ONLINE_STORE_MYSQL_USER"),
        getenv("ONLINE_STORE_MYSQL_PWD"),
        getenv("ONLINE_STORE_MYSQL_HOST"),
        getenv("ONLINE_STORE_MYSQL_DB"),
    )

    app.config["SECRET_KEY"] = "thisidsupposedtobeasecretkey"

    bcrypt.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "app_auth.login"

    # blueprint for authentication routes
    from web_flask.version01.views.authentication_app import app_auth
    app.register_blueprint(app_auth)

    # blueprint for main routes
    from web_flask.version01.views.online_store import app_main

    app.register_blueprint(app_main)

    cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

    @login_manager.user_loader
    def load_user(user_id):
        user = storage.user_by_id(user_id)
        return user

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
