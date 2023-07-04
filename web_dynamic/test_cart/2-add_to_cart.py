#!/usr/bin/python3
"""
    Creating a new view for Cart objects that
    handles all default RESTFul API actions:
"""


from models.cart import Cart
from models.user import User
from models import storage
from flask import jsonify, abort, request, Flask

app = Flask(__name__)


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
    app.run(host='0.0.0.0', port=5002, debug=True)
