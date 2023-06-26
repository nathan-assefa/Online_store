#!/usr/bin/python3

import json
from sys import argv

with open(argv[1]) as file_name:
    categories = json.load(file_name)
    for category in categories:
        #if category == 'dressings':
        for item in categories[category]:
            print(item['name'])

