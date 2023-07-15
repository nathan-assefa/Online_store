#!/usr/bin/python3
"""
    Creating a new view for Review objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.review import Review
from models.user import User
from models.product import Product
from models import storage
from flask import jsonify, abort, request


@app_views.route(
        "/products/<product_id>/reviews", methods=["GET"], strict_slashes=False
        )
def reviews(product_id):
    """ listing all the reviews """
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    return jsonify([review.to_dict() for review in product.reviews])


@app_views.route(
        "/products/<product_id>/reviews", methods=["POST"], strict_slashes=False
        )
def create_review(product_id):
    """ This function retuns and sends reviews from and into database """
    product = storage.get(Product, product_id)
    new_reviews = request.get_json()
    if not product:
        abort(404)

    elif request.method == "POST":
        if not product:
            abort(404)

        if not new_reviews:
            return jsonify({"error": "Not a JSON"}), 400

        elif 'user_id' not in new_reviews:
            return jsonify({"error": "Missing user_id"}), 400

        elif not storage.get(User, new_reviews['user_id']):
            abort(404)

        elif 'comment' not in new_reviews:
            return jsonify({"error": "Missing comment"}), 400

        # adding product_id to keep integrity between products and reviews table
        new_reviews['product_id'] = product_id
        created_review = Review(**new_reviews)
        storage.new(created_review)
        storage.save()

        return jsonify(created_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def review(review_id):
    """This function returns and deletes a review"""
    review = storage.get(Review, review_id)
    if review and request.method == 'GET':
        return jsonify(review.to_dict())

    elif review and request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})

    elif review and request.method == "PUT":
        new_review = request.get_json()

        if not new_review:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_review.items():
            if key not in [
                    'id', 'created_at', 'updated_at', 'user_id', 'product_id'
                    ]:
                setattr(review, key, val)
        storage.save()
        return jsonify(review.to_dict())

    else:
        abort(404)
