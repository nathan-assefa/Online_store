#!/usr/bin/python3


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/shop', strict_slashes=False)
def online_shop():
    url = [
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg',
        'https://s.alicdn.com/@sc04/kf/H3a318e72f6a0453e8001e53a9fc1452ew.jpg_480x480.jpg'
    ]

    return render_template('fauxica.html', urls=url, single=url[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
