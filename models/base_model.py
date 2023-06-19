#!/usr/bin/env python3
""" Implementing the Base class for AirBnB_console """


from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy import String, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel():
    """ This class comprises the common attributes """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """ Returning the instance in user friendly way """
        return "[{}] ({}) {}".format(
                type(self).__name__, self.id, self.to_dict()
                )

    def __repr__(self):
        """ Returning the '__str__' result as a standard python expression """
        return self.__str__()`

    def to_dict(self):
        """
            extracting the attributes of the BaseModel object,
            and put into dict for serilization pupose
        """
        _dict = dict(self.__dict__)
        _dict['__class__'] = self.__class__.__name__
        _dict['created_at'] = self.created_at.isoformat()
        _dict['updated_at'] = self.updated_at.isoformat()
        _dict.pop('_sa_instance_state', None)
        return _dict
    
    """
    def to_dict(self):
        #Extracts the attributes of the BaseModel object and returns a dictionary.

        dict_copy = dict(self.__dict__)
        dict_copy.pop('_sa_instance_state', None)
        return {
            **dict_copy,
            '__class__': self.__class__.__name__,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        The **dict_copy syntax is called dictionary unpacking or
        dictionary merging. It allows us to merge the key-value pairs
        from dict_copy into the new dictionary being constructed. This ensures 
        that the resulting dictionary includes all the attributes from dict_copy,
        in addition to the extra key-value pairs representing the class name,
        created timestamp, and updated timestamp.

        If we omit **dict_copy and simply return a new dictionary with the
        additional key-value pairs, we would lose the attributes from dict_copy.
        In that case, the resulting dictionary would only contain the additional
        key-value pairs we explicitly include in the return statement.
    """
