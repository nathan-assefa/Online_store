#!/usr/bin/python3
from web_content.online_shop.v1.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
