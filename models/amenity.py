#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, Base
import os
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
str_type = os.environ.get("HBNB_TYPE_STORAGE")

class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if str_type == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("place", secondary="place_amenty")
    else:
        name = ""
