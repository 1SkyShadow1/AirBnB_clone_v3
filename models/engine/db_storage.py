#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import os
from sqlalchemy import create_engine, MetaData
from models.base_model import Base
from sqlalchemy.orm import scoped_session, sessionmaker
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """
    will handle long term storage
    of class instances
    """
    Classes = {
            'BaseModel': base_model.BaseModel,
            'Amenity': amenity.Amenity,
            'City' : city.City,
            'Place': place.Place,
            'Review': review.Review,
            'State': state.State,
            'User': user.User
    }
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine( 
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        my_dict = {}
        if cls:
            object_class = self.__session.query(self.Classes.get(cls)).all()
            for i in object_class:
                key = "{}.{}".format(type(i).__name__, i.id)
                my_dict[key] = i
            return my_dict
        for cls_name in self.Classes:
            if cls_name == 'BaseModel':
                continue
            object_class = self.__session.query(
                self.Classes.get(cls_name)).all()
            for i in object_class:
                key = str(i.__class__.__name__) + "." + str(i.id)
                my_dict[key] = i
        return my_dict
            
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def get(self, cls, id):
        """
        will fetch a specific object
        """
        my_classes = self.all(cls)

        for ob in my_classes.values():
            if id == ob.id:
                return ob
        return None

    def count(self, cls=None):
        """
        Will count instances
        of a class
        """
        return len(self.all(cls))

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
