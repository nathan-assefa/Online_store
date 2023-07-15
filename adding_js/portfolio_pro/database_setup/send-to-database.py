#!/usr/bin/python3
import json
from sys import argv
from models import storage
from models.product import Product
from models.category import Category
from models.url import Url


categories = storage.all(Category).values()

category_list = {category.name: category.id for category in categories}

with open(argv[1]) as file_name:
    categories_data = json.load(file_name)

    for category in categories_data:
        for item in categories_data[category]:
            item['category_id'] = category_list.get(category)
            urls = item.pop('url', None)
            new_item = Product(**item)
            storage.new(new_item)
            storage.save()
            for url in urls:
                new_url = {}
                new_url['_type'] = new_item.category.name
                new_url['product_id'] = new_item.id
                new_url['link'] = url
                created_url = Url(**new_url)
                storage.new(created_url)

    storage.save()

"""
In an ORM (Object-Relational Mapping) system like SQLAlchemy, changes made to
objects are typically not persisted to the database until a commit operation is performed.

In this code snippet, new_item.category.name is attempting to access the name attribute of
the category relationship of the new_item object. However, until the changes are committed
and the session is flushed, the relationship might not be loaded, resulting in a None value
for the category attribute.

To ensure that the relationship is loaded and you can access the name attribute, you should 
commit the changes before accessing it. You can do this by adding storage.save() or 
storage.commit() after the storage.new(new_item) line in each category block.

***By the way you do not have to worry about this since it has already been handled :.)****
"""

