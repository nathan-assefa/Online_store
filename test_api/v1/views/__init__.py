#!/usr/bin/python3

from flask import Blueprint

app_test = Blueprint('app_test', __name__, url_prefix='/test_api/v1')
from test_api.v1.views.testing import *
from test_api.v1.views.online_store import *
