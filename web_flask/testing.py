#!/usr/bin/python3


#from models import storage
#from models.product import Product
#from models.category import Category
#from models.url import Url
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/testing', strict_slashes=False)
def online_shop():
    return 'hello world'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
