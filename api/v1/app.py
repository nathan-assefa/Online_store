#!/usr/bin/python3
""" Registering blue prints """

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    import os

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5001"))
    app.run(host=host, port=5001, threaded=True, debug=True)
