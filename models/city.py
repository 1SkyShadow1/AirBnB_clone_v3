#!/usr/bin/python3
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import os
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
str_type = os.environ.get('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """Representation of city """
    if str_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities", cascade='delete')
    else:
        state_id = ""
        name = ""

    if str_type != 'db':
        @property
        def places(self):
            """
            gets places
            """
            all_the_places = models.storage.all("Place")

            res = []

            for ob in  all_the_places.values():
                if str(ob.city_id) == str(self.id):
                    res.append(ob)
