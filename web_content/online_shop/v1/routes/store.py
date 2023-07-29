#!/usr/bin/python3


from models import storage
from models.product import Product
from models.category import Category
from models.url import Url
from flask import Flask, render_template, Blueprint, session
from random import randint
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
import uuid

app_store = Blueprint('app_store', __name__, url_prefix='/store/v1')


@app_store.route('/', strict_slashes=False)
def landing_page():
    cache_id = str(uuid.uuid4())
    return render_template('landing_page.html', cache_id=cache_id)


@app_store.route('/about_us', strict_slashes=False)
def about_us():
    return render_template('about_us.html')


@app_store.route('/cart', strict_slashes=False)
def single_product():
    cache_id = str(uuid.uuid4())
    cart_id = session['cart'].get('id')
    return render_template('cart.html', cart=cart_id, cache_id=cache_id)


@app_store.route('/items', strict_slashes=False)
def single_prodcuct():
    cache_id = str(uuid.uuid4())
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.urls:
            image = product.urls[0].link  # Select the first image
        else:
            image = None
        sort_options = ['name', 'price', 'id', 'created_at', 'updated_at']
        len_options = len(sort_options)
        sort_key = sort_options[randint(0, len_options - 1)]

        products_data.append({
            'name': product.name,
            'image': image,
            'description': product.description,
            'price': product.price,
            'id': product.id,
            'sort_key': sort_key
            })
    # Pass the data to the template
    return render_template('all_product.html', products=products_data, cache_id=cache_id)


@app_store.route('/category/<category_name>', strict_slashes=False)
def categories(category_name):
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.category.name == category_name:
            if product.urls:
                url_length = len(product.urls)
                image = product.urls[randint(0, url_length - 1)].link  # Select the first image
            else:
                image = None

            products_data.append({
                'name': product.name,
                'image': image,
                'description': product.description,
                'price': product.price,
                'id': product.id,
                })
    # Pass the data to the template
    return render_template('categories.html', products=products_data)


# Single Products Page
@app_store.route('/item/<string:product_id>/', strict_slashes=False)
@login_required
def item(product_id):
    cache_id = str(uuid.uuid4())
    product = storage.get(Product, product_id)
    products = storage.all(Product)
    product_data = {}
    related_products_data = []

    if product:
        if product.urls:
            main_image = product.urls[0].link
            images = product.urls
        product_data.update({
            'name': product.name,
            'main_image': main_image,
            'images': images,
            'description': product.description,
            'price': product.price,
            'id': product.id,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'cart_id': session['cart'].get('id')
            })

    for related_product in products.values():
        if related_product.name == product.name and related_product.id != product.id:
            if related_product.urls:
                image = related_product.urls[0].link
            else:
                image = None
            related_products_data.append({
                'name': related_product.name,
                'image': image,
                'description': related_product.description,
                'price': related_product.price,
                'id': related_product.id,
                'category_id': related_product.category.id
                })

    # Pass the data to the template
    return render_template('single_product.html',
            product=product_data,
            related_products=related_products_data,
            cache_id=cache_id
            )
