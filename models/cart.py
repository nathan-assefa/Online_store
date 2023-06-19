#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Cart(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'carts'
   
    user_id = Column(
            String(60),
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False
            )
    cart_itmes = relationship(
            'CartItem',
            backref='cart',
            cascade = "all, delete, delete-orphan"
            )
