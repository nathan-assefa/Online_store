#!/usr/bin/python3


from models import storage
from models.product import Product
from models.category import Category
from models.url import Url
from flask import Flask, render_template, url_for

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
            'price': product.price,
            'id': product.id,
            'category_id': product.category.id
            })
    # Pass the data to the template
    return render_template('index.html', products=products_data)

@app.route('/item/<string:category_id>/<string:product_id>/<string:product_name>', strict_slashes=False)
def item(category_id, product_id, product_name):
    products = storage.all(Product)
    products_data = []
    related_products_data = []

    for product in products.values():
        if product.id == product_id:
            if product.urls:
                main_image = product.urls[0]
                images = product.urls
            products_data.append({
                'name': product.name,
                'main_image': main_image,
                'images': images,
                'description': product.description,
                'price': product.price,
                'id': product.id,
                'category_id': product.category.id
                })
            break
    for related_products in products.values():
        if related_products.category_id == category_id:
            if related_products.urls:
                image = related_products.urls[0].link
            else:
                image = None
            if not related_products.id == product_id:
                if related_products.name == product_name:
                    related_products_data.append({
                        'name': related_products.name,
                        'image': image,
                        'description': related_products.description,
                        'price': related_products.price,
                        'id': related_products.id,
                        'category_id': related_products.category.id
                        })

    # Pass the data to the template
    #return render_template('single_item.html',
    return render_template('product_item.html',
            products=products_data[0],
            related_products=related_products_data
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
