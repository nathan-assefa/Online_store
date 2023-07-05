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

@app.route('/cart', strict_slashes=False)
def online_shop():
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
    return render_template('index.html', products=products_data)

@app.route('/order_page', strict_slashes=False)
def order_page():
    return render_template('cart.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
