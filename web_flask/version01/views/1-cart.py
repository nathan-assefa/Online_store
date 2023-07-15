#!/usr/bin/python3


from models import storage
from models.product import Product
from models.category import Category
from models.url import Url
from flask import Flask, render_template

app = Flask(__name__)

@app.teardown_appcontext
def close_db(exit):
    """This context function gives back the
    connection once request is done"""
    storage.close()


@app.route('/', strict_slashes=False)
def landing_page():
    return render_template('landing_page.html')

'''
@app.route('/product', strict_slashes=False)
def single_product():
    return render_template('single_product.html')
'''


@app.route('/items', strict_slashes=False)
def single_prodcuct():
    products = storage.all(Product)
    products_data = []

    for product in products.values():
        if product.urls:
            image = product.urls[0].link  # Select the first image
        else:
            image = None

        products_data.append({
            'name': product.name,
            'image': image,
            'description': product.description,
            'price': product.price,
            'id': product.id
            })
    # Pass the data to the template
    return render_template('all_product.html', products=products_data)


@app.route('/order_page', strict_slashes=False)
def order_page():
    return render_template('cart.html')


# Single Products Page
@app.route('/item/<string:product_id>/', strict_slashes=False)
def item(product_id):
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
            'category_name': product.category.name
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
            related_products=related_products_data
            )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
