#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
#import models
from sqlalchemy import Column, String, Integer, ForeignKey


class CartItem(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'cart_items'

    quantity = Column(Integer, nullable=False)
    cart_id = Column(
            String(60),
            ForeignKey('carts.id', ondelete='CASCADE'),
            nullable=False
            )

    product_id = Column(
            String(60),
            ForeignKey('products.id', ondelete='CASCADE'),
            nullable=False
            )

    #usr_id = '7f13bc83-5a3b-4f7b-b662-d870b8c36c73'
    #ord_id = 'c842de02-4351-466b-8a5d-64d76dae5ff2'
    #models.storage.create_order_items(usr_id, ord_id)
