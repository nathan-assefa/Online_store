#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
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
