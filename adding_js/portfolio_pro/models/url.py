#!/usr/bin/python3
""" Definig a user class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Url(BaseModel, Base):
    """Defining a user class"""

    __tablename__ = "urls"

    _type = Column(String(60), nullable=True)
    link = Column(String(128), nullable=False)
    product_id = Column(
            String(60),
            ForeignKey('products.id', ondelete="CASCADE"),
            nullable=False
            )
