#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
import os
import sqlalchemy
from sqlalchemy import Column,Integer, String, Float
from sqlalchemy.orm import relationship
str_type = os.environ.get('HBNB_TYPE_STORAGE')

class State(BaseModel, Base):
    """Representation of state """
    if str_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    if str_type != 'db':
        @property
        def cities(self):
            city_list = []
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
