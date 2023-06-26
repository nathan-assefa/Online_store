#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'categories'
   
    name = Column(String(128), nullable=False)
    #quantity = Column(Integer, nullable=False)
    products = relationship(
            'Product',
            backref='category',
            cascade = "all, delete, delete-orphan"
            )
