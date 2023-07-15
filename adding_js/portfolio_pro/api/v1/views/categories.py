#!/usr/bin/python3
""" Defining routes for the categoriy table """


from api.v1.views import app_views
from models import storage
from models.category import Category
from flask import jsonify, request, abort


@app_views.route('/categories', strict_slashes=False)
def categories():
    """ List all the category instances """
    _dict = [category.to_dict() for category in storage.all(Category).values()]
    return jsonify(_dict)


@app_views.route('/categories/<category_id>', strict_slashes=False)
def category(category_id):
    """ gets a singel category instance from categories table """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    return jsonify(category.to_dict())


@app_views.route(
        '/categories/<category_id>', methods=['Delete'], strict_slashes=False
        )
def delete_category(category_id):
    """ delete a catagory instance """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    storage.delete(category)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/categories', methods=['POST'], strict_slashes=False
        )
def category_post():
    """ Adding catagory row in the categories table """
    # Checking if the request is json formated
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    # since the request is json formated, we parse it to python dict
    category = request.get_json()

    # here we check if the data contains the 'name' key
    if "name" not in category.keys():
        return jsonify({"error": "Missing Name"}), 400

    #elif "quantity" not in category.keys():
        #return jsonify({"error": "Missing Quantity"}), 400

    # here send the new created category to the database and  commit
    created_category = Category(**request.get_json())
    storage.new(created_category)
    storage.save()

    return jsonify(created_category.to_dict()), 201


@app_views.route(
        '/categories/<category_id>', methods=['PUT'], strict_slashes=False
        )
def category_put(category_id):
    """ Updating category instance """

    category = storage.get(Category, category_id)
    new_data = request.get_json()

    if not category:
        abort(404)

    if not new_data:
        return jsonify({"error": "Not a Json"}), 400

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(category, key, value)

    # Save the updated user object to the database
    storage.save()
    return jsonify(category.to_dict())
