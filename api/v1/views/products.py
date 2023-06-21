#!/usr/bin/python3
"""
    Creating a new view for Product objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.product import Product
from models.category import Category
from models import storage
from flask import jsonify, abort, request


@app_views.route("/categories/<category_id>/products", strict_slashes=False)
def get_products(category_id):
    """ Getting products via their categoriy """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    _dict = [product.to_dict() for product in category.products]
    return jsonify(_dict)


@app_views.route(
        "/categories/<category_id>/products",
        methods=['POST'],
        strict_slashes=False
        )
def post_product(category_id):
    """ This function sends product into database """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    product = request.get_json()

    if "name" not in product.keys():
        return jsonify({"error": "Missing name"}), 400

    if "price" not in product.keys():
        return jsonify({"error": "Missing price"}), 400

    # here we send the new created product to the database and  commit
    new_product = request.get_json()
    # adding category_id to keep integrity between
    # categories and productis table
    new_product['category_id'] = category_id
    created_product = Product(**new_product)
    storage.new(created_product)
    storage.save()

    return jsonify(created_product.to_dict()), 201


@app_views.route(
        "/products/<product_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def product(product_id):
    """This function returns and deletes a product"""
    product = storage.get(Product, product_id)
    if product and request.method == 'GET':
        return jsonify(product.to_dict())

    elif product and request.method == "DELETE":
        product.delete()
        storage.save()
        return jsonify({})

    elif product and request.method == "PUT":
        new_product = request.get_json()

        if not new_product:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_product.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(product, key, val)
        storage.save()
        return jsonify(product.to_dict())

    else:
        abort(404)
