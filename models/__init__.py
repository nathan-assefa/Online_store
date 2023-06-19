#!/usr/bin/python3
from os import environ

from models.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()
