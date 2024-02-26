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
        id = Column(String(60), primary_key=True, nullable=False)
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
