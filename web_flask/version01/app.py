#!/usr/bin/python3
""" Flask Application """
from os import getenv
from models import storage
from web_flask.version01.views import app_views
from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS


"""
db = SQLAlchemy()
bcrypt = Bcrypt()
"""

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://{}:{}@{}/{}'.format(
        getenv('ONLINE_STORE_MYSQL_USER'),
        getenv('ONLINE_STORE_MYSQL_PWD'),
        getenv('ONLINE_STORE_MYSQL_HOST'),
        getenv('ONLINE_STORE_MYSQL_DB')
        )

app.config["SECRET_KEY"] = "thisidsupposedtobeasecretkey"


"""
db = SQLAlchemy()
bcrypt = Bcrypt()
"""
"""
db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user = storage.user_by_id(user_id)
    return user
"""
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(exit):
    """This context function gives back the
    connection once request is done"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    #return render_template("404.html")
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
