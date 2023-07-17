'''

#!/usr/bin/python3


from flask import Blueprint


app_store = Blueprint('app_store', __name__, url_prefix='store/v1')
from web_content.online_shop.v1.routes.store import *
'''
