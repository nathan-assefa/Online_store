#!/usr/bin/python3
""" Blueprint"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/gebeya_hub/version01')


from web_flask.version01.views.index import *
from web_flask.version01.views.online_store import *
from web_flask.version01.views.authentication_app import *
