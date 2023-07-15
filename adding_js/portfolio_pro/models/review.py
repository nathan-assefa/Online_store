#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint


class Review(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'reviews'

    comment = Column(String(1024), nullable=False)
    rating = Column(
            Integer,
            CheckConstraint('rating >= 0 AND rating <= 5'),
            default=0)
    product_id = Column(
            String(60),
            ForeignKey('products.id', ondelete='CASCADE'),
            nullable=False
            )
    user_id = Column(
            String(60),
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False
            )
