#!/usr/bin/python3
""" This script lets the flask app connects to mysql database and
fetch all the data from the states table.

ip address 0.0.0.0 is used to allow all the network interface ip
addresses to have access to our app. Port 5000 will be used at entry
point """


from flask import Flask, render_template
from models.product import Product
from models import storage
import uuid


app = Flask(__name__)


@app.teardown_appcontext
def close_db(exit):
    """This context function gives back the
    connection once request is done"""
    storage.close()


@app.route("/cart", strict_slashes=False)
def db_app():
    product = storage.get(Product, 'e599a11b-86a4-421c-bfac-86ed7d5e1181')

    if product.urls:
        image = product.urls[0].link  # Select the first image
    else:
        image = None

    return render_template(
            "index.html",
            name=product.name,
            image=image,
            price=product.price,
            id=product.id
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
