#!/usr/bin/python3

import json
from sys import argv

with open(argv[1]) as file_name:
    f = json.load(file_name)
    for category in f:
        if category == 'tech':
            for item in f[category]:
                print(item['name'])

