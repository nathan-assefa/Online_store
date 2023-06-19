#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """ Defining a user class """
    __tablename__ = 'orders'

    order_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    user_id = Column(
            String(60),
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False
            )
    order_itmes = relationship(
            'OrderItem',
            backref='order',
            cascade = "all, delete, delete-orphan"
            )
