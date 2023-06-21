#!/usr/bin/python3
"""
    Creating a new view for Cart objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.cart import Cart
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users/<user_id>/carts", strict_slashes=False)
def get_carts(user_id):
    """ Getting carts via their categoriy """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    _dict = [cart.to_dict() for cart in user.carts]
    return jsonify(_dict)


@app_views.route(
        "/users/<user_id>/carts",
        methods=['POST'],
        strict_slashes=False
        )
def post_cart(user_id):
    """ This function sends cart into database """
    user = storage.get(User, user_id)
    new_cart = {}

    if not user:
        abort(404)

    # adding user_id to keep integrity between
    # users and carts table
    new_cart['user_id'] = user_id
    created_cart = Cart(**new_cart)
    storage.new(created_cart)
    storage.save()

    return jsonify(created_cart.to_dict()), 201


@app_views.route(
        "/carts/<cart_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def cart(cart_id):
    """This function returns and deletes a cart"""
    cart = storage.get(Cart, cart_id)
    if cart and request.method == 'GET':
        return jsonify(cart.to_dict())

    elif cart and request.method == "DELETE":
        cart.delete()
        storage.save()
        return jsonify({})

    elif cart and request.method == "PUT":
        new_cart = request.get_json()

        if not new_cart:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_cart.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(cart, key, val)
        storage.save()
        return jsonify(cart.to_dict())

    else:
        abort(404)
