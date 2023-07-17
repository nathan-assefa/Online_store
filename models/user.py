#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'users'
    
    first_name = Column(String(128), nullable=True)
    Last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    reviews = relationship(
            'Review',
            backref='user',
            cascade='all, delete, delete-orphan'
            )
    carts = relationship(
            'Cart',
            backref='user',
            cascade='all, delete, delete-orphan'
            )
    orders = relationship(
            'Order',
            backref='user',
            cascade='all, delete, delete-orphan'
            )
