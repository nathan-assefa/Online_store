#!/usr/bin/python3
"""
    Creating a new view for Product objects that
    handles all default RESTFul API actions:
"""


from test_api.v1.views import app_test
from models.product import Product
from models import storage
from flask import render_template


@app_test.route("/products/<product_id>", strict_slashes=False)
def product(product_id):
    product = storage.get(Product, product_id)
    all_products = storage.all(Product).values()
    category_name = ""
    related_products = []

    for pro in all_products:
        if pro.category.name == product.category.name:
            for url in pro.urls[:1]:
                related_products.append(url.link)
    if product.category.name == 'dressings':
        category_name = "Glamourra"
    elif product.category.name == 'shoe':
        category_name = "Footsorcery"
    elif product.category.name == 'jewelry':
        category_name = "Glimmera"
    elif product.category.name == 'tech':
        category_name = "Technomancy"

    images = [url.link for url in product.urls]

    return render_template(
            'sub_page.html',
            images=images,
            product=product,
            category_name=category_name,
            related_products=related_products
            )
