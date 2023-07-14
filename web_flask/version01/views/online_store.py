#!/usr/bin/python3
""" app module """


from models import storage
from models.product import Product
from models.category import Category
from models.user import User
from models.url import Url
import sys
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    make_response,
)
from flask import Blueprint


app_main = Blueprint("app_main", __name__, url_prefix="/gebeya_hub/version01")

# Landing Page
@app_main.route("/", strict_slashes=False)
def landing_page():
    return render_template("landing_page.html")


# About us page
@app_main.route("/about_us", strict_slashes=False)
def about_us():
    return render_template("about-us_page.html")


# Home Page
@app_main.route("/shop", strict_slashes=False)
def online_shop():
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.urls:
            image = product.urls[0].link  # Select the first image
        else:
            image = None
        products_data.append(
            {
                "name": product.name,
                "image": image,
                "description": product.description,
                "price": product.price,
                "id": product.id,
                "category_id": product.category.id,
            }
        )
    # Pass the data to the template
    # return render_template('index.html', products=products_data)
    return render_template("home_page.html", products=products_data)


# Single Products Page
@app_main.route("/item/<string:product_id>/", strict_slashes=False)
def item(product_id):
    product = storage.get(Product, product_id)
    products = storage.all(Product)
    product_data = {}
    related_products_data = []

    if product:
        if product.urls:
            main_image = product.urls[0].link
            images = product.urls
        product_data.update(
            {
                "name": product.name,
                "main_image": main_image,
                "images": images,
                "description": product.description,
                "price": product.price,
                "id": product.id,
                "category_id": product.category.id,
            }
        )

    for related_product in products.values():
        if related_product.name == product.name and related_product.id != product.id:
            if related_product.urls:
                image = related_product.urls[0].link
            else:
                image = None
            related_products_data.append(
                {
                    "name": related_product.name,
                    "image": image,
                    "description": related_product.description,
                    "price": related_product.price,
                    "id": related_product.id,
                    "category_id": related_product.category.id,
                }
            )

    # Pass the data to the template
    return render_template(
        "product_item.html",
        product=product_data,
        related_products=related_products_data,
    )


# Products in main catagories
@app_main.route("/items/<string:category_id>")
def category(category_id):
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.category_id == category_id:
            if product.urls:
                image = product.urls[0].link  # Select the first image
            else:
                image = None

                products_data.append(
                    {
                        "name": product.name,
                        "image": image,
                        "description": product.description,
                        "price": product.price,
                        "id": product.id,
                        "category_id": product.category.id,
                    }
                )
    # Pass the data to the template
    return render_template("index.html", products=products_data)
