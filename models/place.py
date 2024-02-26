#!/usr/bin/python3
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
import os
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

str_type = os.environ.get('HBNB_TYPE_STORAGE')


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Place(BaseModel, Base):
    """Representation of Place """
    if models.storage_t == 'db':
        __tablename__ = 'places'
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
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []


    if str_type != 'db':
        @property
        def amenities(self):
            """
            gets ammenities
            """
            amen_obj = []

            for amen_id in self.amenity_ids:
                amen_obj.append(models.storage.get('Amenity', str(amen_id)))

            return amen_obj

        @amenities.setter
        def amenities(self, amenity):
            """
            sets ammenities
            """
            self.amenity_ids.append(amenity.id)

        @property
        def reviews(self):
            """
            gets reviews
            """
            all_revs = models.storage.get('Review')
            place_revs = []

            for revs in all_revs.values():
                if revs.place_id == self.id:
                    place_revs.append(revs)

            return place_revs

