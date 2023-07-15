#!/usr/bin/python3
"""
    Creating a new view for OrderItem objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.order_item import OrderItem
from models.user import User
from models.order import Order
from models import storage
from flask import jsonify, abort, request


@app_views.route(
        "/orders/<order_id>/order_items", methods=["GET"], strict_slashes=False
        )
def order_items(order_id):
    """ listing all the order_items """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)
    return jsonify([order_item.to_dict() for order_item in order.order_items])


@app_views.route(
        "/orders/<order_id>/order_items",
        methods=["POST"], strict_slashes=False
        )
def create_order_item(order_id):
    """ This function retuns and sends order_items from and into database """
    order = storage.get(Order, order_id)
    order_data = request.get_json()

    if not order:
        abort(404)
    if not order_data:
        return jsonify({"error": "Not a JSON"}), 400

    elif not storage.get(User, order_data['user_id']):
        abort(404)

    user_id = order_data['user_id']

    new_order = storage.create_order_items(user_id, order_id)

    # here we do not use 'to_dict()' method to serialize the instance
    # since it has already been serialized in the 'create_order_items'
    # method. check the engine out and see the implementation of the method
    return jsonify(new_order), 201


@app_views.route(
        "/order_items/<order_item_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def order_item(order_item_id):
    """This function returns and deletes a order_item"""
    order_item = storage.get(OrderItem, order_item_id)
    if order_item and request.method == 'GET':
        return jsonify(order_item.to_dict())

    elif order_item and request.method == "DELETE":
        order_item.delete()
        storage.save()
        return jsonify({})

    elif order_item and request.method == "PUT":
        new_order_item = request.get_json()

        if not new_order_item:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_order_item.items():
            if key not in [
                    'id', 'created_at',
                    'updated_at', 'product_id', 'order_id'
                    ]:
                setattr(order_item, key, val)
        storage.save()
        return jsonify(order_item.to_dict())

    else:
        abort(404)
