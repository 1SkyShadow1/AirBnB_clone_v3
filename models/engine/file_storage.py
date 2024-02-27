#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from datetime import datetime
from models import base_model, amenity, city, place, review, state,user

strptime = datetime.srptime
to_json = base_model.BaseModel.to_json

class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
    Classes = {
            'BaseModel': base_model.BaseModel,
            'Amenity': amenity.Amenity,
            'City': city.City,
            'Place': place.Place,
            'Review': review.Review,
            'State': state.State,
            'User': user.User
}
    
    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls:
            obj_dict = {}
            for cls_id, ob in FileStorage.__objects.items():
                if type(ob).__name__ == cls:
                    obj_dict[cls_id] = ob
            return obj_dict
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            base_model_id = f"{},{}".format(type(obj), obj.id)
            FileStorage.__objects[base_model_id] = obj

    def get(self, cls, id):
        """
        will get a  specific
        object
        """
        my_classes = self.all(cls)

        for ob in my_classes.values():
            if id == str(ob.id):
                return ob

        return None

    def count(self, cls=None):
        """
        will count instances
        """
        return len(self.all(cls))

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        file_name = FileStorage.__file_path
        dicto = {}
        for bsm_id, bsm_ob in FileStorage.__objects.items():
            dicto[bsm_id] = bsm_ob.to_json()
        with open(file_name, mode='w+', encoding =  'utf-8') as f:
            json.dump(dicto, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        file_name = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(file_name,mode='r', encoding='utf=8') as f:
                n_obs = json.load(f)
            except:
                return
            for obj_id, dicto in n_obs.items():
                class_name = dicto['__class__']
                dicto.pop('__class__', None)
                dicto['created_at'] = datetime.strptime(dicto['created_at'],
                                                        "%Y-%m-%d %H:%M:%S.%f")
                dicto['updated_at'] = daterime.strptime(dicto['updated_at'],
                                                        "%Y-%m-%d %H:%M:%S.%f")
                FileStorage.__objects[obj_id] = FileStorage.Classes(**dicto)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is None:
            return
        for key in list(FileStorage.__objects.keys()):
            if obj.id = key.splits('.')[1] and key.split('.')[0] in str(obj):
                FileStorage.__objects.pop(key, None)
                self.save()

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
