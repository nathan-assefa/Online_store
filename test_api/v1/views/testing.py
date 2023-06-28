#!/usr/bin/python3
"""
    Creating a new view for Url objects that
    handles all default RESTFul API actions:
"""


from test_api.v1.views import app_test
from models.url import Url
from models.product import Product
from models import storage
from flask import jsonify, abort, request


@app_test.route("/products", strict_slashes=False)
def get_urls():
    """ Getting urls via their categoriy """
    #product = storage.get(Product, product_id)

    return "hello world"
