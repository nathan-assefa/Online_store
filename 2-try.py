from models import storage
from models.product import Product
from models.category import Category

categories = storage.all(Category)


