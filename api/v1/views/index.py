#!/usr/bin/python3
""" This script comprises a flask application """


from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def _json():
    _dict = {"status": "OK"}
    return jsonify(_dict)
