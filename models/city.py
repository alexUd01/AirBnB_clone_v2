#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60),  ForeignKey('states.id'), nullable=False)

    # Uncomment the line below this line if checker fails
    # states = relationship('State', backref='cities')
