#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import os
import json
import models
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4, UUID
 
str_type = os.environ.get('HBNB_TYPE_STORAGE')

if models.storage_t == "db":
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False, 
                            default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, 
                            default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            
    def __is_serializable(self, obj):
        """
        Will caheck if obj is serializeable
        """
        try:
            obj_to_string = json.dumps(obj)
            return obj_to_string is not None and isinstance(obj_to_str, str)
        except:
            return False

    def base_model_update(self, name, value):
        """
        will update the basemodel
        """
        setattr(self, name, value)
        if str_type != 'db':
            self.save()

    def save(self):
        """
        will save
        """
        if str_type != 'db':
            self.update_at = datetime.now()
            models.storage.new(self)
            models.storage.save()

    def to_json(self):
        """
        will show representation of self 
        in json
        """
        basemodel_dict = {}
        for k, v in (self.__dict__).items():
            if (self.__is_serializable(v)):
                basemodel_dict[k] = v
            else:
                basemodel_dict[k] = str(v)
        basemodel_dict['__class__'] = type(self).__name__
        if '_sa_insatance_state' in basemodel_dict:
            basemodel_dict.pop('sa_insatnce_state')
        if str_type == 'db' and 'password' in basemodel_dict:
            basemodel_dict.pop('password')
        return basemodel_dict

    def __str__(self):
        """
        will return string form of
        instance
        """
        class_name = type(self).__name__
        return f"[{class_name}] {(self.id)} {self.__dict__}"

    def delete(self):
        """
        Will deltete current
        instance of storage
        """
        self.delete()
