#!/usr/bin/python3
""" Defining routes for the categoriy table """


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', strict_slashes=False)
def users():
    """ List all the user instances """
    _dict = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(_dict)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user(user_id):
    """ gets a singel user instance from users table """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['Delete'], strict_slashes=False
        )
def delete_user(user_id):
    """ delete a user instance """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/users', methods=['POST'], strict_slashes=False
        )
def user_post():
    """ Adding user row in the users table """
    # Checking if the request is json formated
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    # since the request is json formated, we parse it to python dict
    user = request.get_json()

    # here we check if the data contains the 'name' key
    if "email" not in user.keys():
        return jsonify({"error": "Missing Name"}), 400

    elif "password" not in user.keys():
        return jsonify({"error": "Missing Password"}), 400

    # here send the new created user to the database and  commit
    created_user = User(**request.get_json())
    storage.new(created_user)
    storage.save()

    return jsonify(created_user.to_dict()), 201


@app_views.route(
        '/users/<user_id>', methods=['PUT'], strict_slashes=False
        )
def user_put(user_id):
    """ Updating user instance """

    user = storage.get(User, user_id)
    new_data = request.get_json()

    if not user:
        abort(404)

    if not new_data:
        return jsonify({"error": "Not a Json"}), 400

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    # Save the updated user object to the database
    storage.save()
    return jsonify(user.to_dict())
