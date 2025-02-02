#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
str_type = os.environ.get("HBNB_TYPE_STORAGE")

class User(BaseModel, Base):
    """Representation of a user """
    if str_type == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        A password getter
        Return: Password
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, passwoed):
        """
        Passwoord setter
        Return: nothing
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexidigest()
