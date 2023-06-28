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

@app.route('/shop', strict_slashes=False)
def online_shop():
    products = storage.all(Product)
    products_data = []
    '''
    categories_data = storage.all(Category).values()

    category_list = {category.name: category.id for category in categories}
    products_data = []
    dressings = {}
    shoe = {}
    jewelry = {}
    tech = {}
    
    for category in categories_data:
        for item in categories_data[category]:
            print(item)
    '''

    for product in products.values():
        if product.urls:
            image = product.urls[0].link  # Select the first image
        else:
            image = None

        products_data.append({
            'name': product.name,
            'image': image,
            'description': product.description,
            'price': product.price
            })
    # Pass the data to the template
    return render_template('index.html', products=products_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
