#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float


class OrderItem(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'order_items'

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_id = Column(
            String(60),
            ForeignKey('orders.id', ondelete='CASCADE'),
            nullable=False
            )

    product_id = Column(
            String(60),
            ForeignKey('products.id', ondelete='CASCADE'),
            nullable=False
            )
