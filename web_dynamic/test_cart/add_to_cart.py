#!/usr/bin/python3
"""
    Creating a new view for CartItem objects that
    handles all default RESTFul API actions:
"""


from models.cart_item import CartItem
from models.product import Product
from models.cart import Cart
from models import storage
from flask import jsonify, abort, request, Flask

from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"*": {"origins": "*"}})


@app.route(
        "/carts/<cart_id>/cart_items", methods=["GET"], strict_slashes=False
        )
def cart_items(cart_id):
    """ listing all the cart_items """
    cart = storage.get(Cart, cart_id)
    if not cart:
        abort(404)
    return jsonify([cart_item.to_dict() for cart_item in cart.cart_items])


@app.route(
        "/carts/<cart_id>/cart_items", methods=["POST"], strict_slashes=False
        )
def create_cart_item(cart_id):
    """ This function retuns and sends cart_items from and into database """
    cart = storage.get(Cart, cart_id)
    new_cart_items = request.get_json()
    if not cart:
        abort(404)

    elif request.method == "POST":
        if not cart:
            abort(404)

        if not new_cart_items:
            return jsonify({"error": "Not a JSON"}), 400

        elif 'product_id' not in new_cart_items:
            return jsonify({"error": "Missing product_id"}), 400

        elif not storage.get(Product, new_cart_items['product_id']):
            abort(404)

        elif 'quantity' not in new_cart_items:
            return jsonify({"error": "Missing quantity"}), 400

        # adding cart_id to keep integrity between carts and cart_items table
        new_cart_items['cart_id'] = cart_id
        created_cart_item = CartItem(**new_cart_items)
        storage.new(created_cart_item)
        storage.save()

        return jsonify(created_cart_item.to_dict()), 201


@app.route(
        "/cart_items/<cart_item_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def cart_item(cart_item_id):
    """This function returns and deletes a cart_item"""
    cart_item = storage.get(CartItem, cart_item_id)
    if cart_item and request.method == 'GET':
        return jsonify(cart_item.to_dict())

    elif cart_item and request.method == "DELETE":
        cart_item.delete()
        storage.save()
        return jsonify({})

    elif cart_item and request.method == "PUT":
        new_cart_item = request.get_json()

        if not new_cart_item:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_cart_item.items():
            if key not in [
                    'id', 'created_at', 'updated_at', 'product_id', 'cart_id'
                    ]:
                setattr(cart_item, key, val)
        storage.save()
        return jsonify(cart_item.to_dict())

    else:
        abort(404)

from models.cart import Cart
from models.user import User

@app.route("/users/<user_id>/carts", strict_slashes=False)
def get_carts(user_id):
    """ Getting a user carts """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    _dict = [cart.to_dict() for cart in user.carts]
    return jsonify(_dict)


@app.route(
        "/users/<user_id>/carts", methods=['POST'], strict_slashes=False
        )
def post_cart(user_id):
    """ This function creates a new cart for a user sends cart into database """
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


@app.route(
        "/carts/<cart_id>",
        methods=["GET", "DELETE"],
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

    else:
        abort(404)

@app.route('/carts/<cart_id>', methods=['PUT'], strict_slashes=False)
def update_cart_status(cart_id):
    # Retrieve the cart from the database
    cart = storage.get(Cart, cart_id)

    if not cart:
        abort(404)

    # Retrieve the new status value from the request body
    new_status = request.get_json('status')

    if not new_status:
        return jsonify({'error': 'Not a Json'})

    # Update the cart's status
    cart.status = new_status['status']

    # Save the changes to the database
    storage.save()

    return jsonify(cart.to_dict()), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
