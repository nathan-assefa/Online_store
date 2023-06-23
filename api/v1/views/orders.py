#!/usr/bin/python3
"""
    Creating a new view for Order objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.order import Order
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users/<user_id>/orders", strict_slashes=False)
def get_orders(user_id):
    """ Getting a user orders """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    _dict = [order.to_dict() for order in user.orders]
    return jsonify(_dict)


@app_views.route(
        "/users/<user_id>/orders", methods=['POST'], strict_slashes=False
        )
def post_order(user_id):
    """ This function creates a new order for a user sends order into database """
    user = storage.get(User, user_id)
    new_order = {}

    if not user:
        abort(404)

    # adding user_id to keep integrity between
    # users and orders table
    new_order['user_id'] = user_id
    created_order = Order(**new_order)
    storage.new(created_order)
    storage.save()

    return jsonify(created_order.to_dict()), 201


@app_views.route(
        "/orders/<order_id>",
        methods=["GET", "DELETE"],
        strict_slashes=False
        )
def order(order_id):
    """This function returns and deletes a order"""
    order = storage.get(Order, order_id)
    if order and request.method == 'GET':
        return jsonify(order.to_dict())

    elif order and request.method == "DELETE":
        order.delete()
        storage.save()
        return jsonify({})

    else:
        abort(404)

@app_views.route('/orders/<order_id>', methods=['PUT'], strict_slashes=False)
def update_order_status(order_id):
    # Retrieve the order from the database
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    # Retrieve the new status value from the request body
    new_status = request.get_json('status')

    if not new_status:
        return jsonify({'error': 'Not a Json'}) 

    # Update the order's status
    order.status = new_status['status']

    # Save the changes to the database
    storage.save()

    return jsonify(order.to_dict()), 200
