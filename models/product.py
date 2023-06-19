#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'products'

    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(1024))
    category_id = Column(String(60),
            ForeignKey('categories.id', ondelete='CASCADE'),
            nullable=False
            )
    reviews = relationship(
            'Review',
            backref='product',
            cascade='all, delete, delete-orphan'
            )
