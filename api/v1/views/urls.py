#!/usr/bin/python3
"""
    Creating a new view for Url objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.url import Url
from models.product import Product
from models import storage
from flask import jsonify, abort, request


@app_views.route("/products/<product_id>/urls", strict_slashes=False)
def get_urls(product_id):
    """ Getting urls via their categoriy """
    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    _dict = [url.to_dict() for url in product.urls]
    return jsonify(_dict)


@app_views.route(
        "/products/<product_id>/urls",
        methods=['POST'],
        strict_slashes=False
        )
def post_url(product_id):
    """ This function sends url into database """
    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    url = request.get_json()

    if "name" not in url.keys():
        return jsonify({"error": "Missing name"}), 400

    if "price" not in url.keys():
        return jsonify({"error": "Missing price"}), 400

    # here we send the new created url to the database and  commit
    new_url = request.get_json()
    # adding product_id to keep integrity between
    # products and urlis table
    new_url['product_id'] = product_id
    created_url = Url(**new_url)
    storage.new(created_url)
    storage.save()

    return jsonify(created_url.to_dict()), 201


@app_views.route(
        "/urls/<url_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def url(url_id):
    """This function returns and deletes a url"""
    url = storage.get(Url, url_id)
    if url and request.method == 'GET':
        return jsonify(url.to_dict())

    elif url and request.method == "DELETE":
        url.delete()
        storage.save()
        return jsonify({})

    elif url and request.method == "PUT":
        new_url = request.get_json()

        if not new_url:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_url.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(url, key, val)
        storage.save()
        return jsonify(url.to_dict())

    else:
        abort(404)
