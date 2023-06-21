#!/usr/bin/python3
"""
    Creating a new view for Cart objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.order import Order
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users/<user_id>/orders", strict_slashes=False)
def get_orders(user_id):
    """ Getting orders via their categoriy """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    _dict = [order.to_dict() for order in user.orders]
    return jsonify(_dict)


@app_views.route(
        "/users/<user_id>/orders",
        methods=['POST'],
        strict_slashes=False
        )
def post_order(user_id):
    """ This function sends order into database """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    order = request.get_json()

    if "name" not in order.keys():
        return jsonify({"error": "Missing name"}), 400

    if "price" not in order.keys():
        return jsonify({"error": "Missing price"}), 400

    # here we send the new created order to the database and  commit
    new_order = request.get_json()
    # adding user_id to keep integrity between
    # users and orderis table
    new_order['user_id'] = user_id
    created_order = Cart(**new_order)
    storage.new(created_order)
    storage.save()

    return jsonify(created_order.to_dict()), 201


@app_views.route(
        "/orders/<order_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def order(order_id):
    """This function returns and deletes a order"""
    order = storage.get(Cart, order_id)
    if order and request.method == 'GET':
        return jsonify(order.to_dict())

    elif order and request.method == "DELETE":
        order.delete()
        storage.save()
        return jsonify({})

    elif order and request.method == "PUT":
        new_order = request.get_json()

        if not new_order:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_order.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(order, key, val)
        storage.save()
        return jsonify(order.to_dict())

    else:
        abort(404)
