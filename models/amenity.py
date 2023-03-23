#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models import storage_type


class Amenity(BaseModel, Base):
    """ Fundamental/Basic Amenities """

    __tablename__ = 'amenities'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ''
