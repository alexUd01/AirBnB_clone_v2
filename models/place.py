#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table


metadata = Base.metadata
place_amenity = Table(
    'place_amenity', metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'), nullable=False,
           primary_key=True),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'), nullable=False,
           primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenity_ids = []

    reviews = relationship('Review', backref='place')
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False, backref='places')

    @property
    def reviews(self):
        """ Returns the list of Review instances whose place_id is equal to
        the current place.id
        """
        from models import storage

        result = []
        for k, v in storage.all(Review).items():
            if k.split('.')[1] == self.id:
                result.append(v)

        return result

    @property
    def amenities(self):
        """ Returns the list of Amenity instances based on the attribute
        ammenity_ids that contains all Amenity.id linked to Place
        """
        from models import storage
        from models.amenity import Amenity

        lst = []
        for item in storage.all(Amenity).values():
            if item.id in Place.amenity_ids:
                lst.append(item)
        return lst

    @amenities.setter
    def amenities(self, Amenity_obj):
        """ Handles append method for adding Amenity.id to the attribute
        amenity_id.
        """
        if isinstance(Amenity_obj, Amenity):
            Place.amenity_ids.append(Amenity.id)
