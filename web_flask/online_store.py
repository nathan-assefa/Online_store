#!/usr/bin/python3


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/shop', strict_slashes=False)
def online_shop():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
