#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
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
