#!/usr/bin/python3

"""
Handles Amenity
objects and operations
"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views, storage


@app_views.route("/amenities", methods=["Get"],
                 strict_slashes=False)
def amenity_acq_all():
    """
    Will get Amenity
    objects
    """
    amenity_list = []
    amenity_obj = storage.all("Amenity")
    for ob in amenity_obj.values():
        amenity_list.append(ob.to_json())

    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def amenity_make():
    """
    Will create an amenity route
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    response = jsonify(new_amenity.to_json())
    response.status_code = 201

    return response


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """
    Will get a specific
    Amenity object using Id
    """

    got_obj = storage.get("Amenity", str(amenity_id))

    if got_obj is None:
        abort(404)

    return jsonify(got_obj.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put_id(amenity_id):
    """
    Will update an Amenity object
    using id
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    got_obj = storage.get("Amenity", str(amenity_id))
    if got_obj is None:
        abort(400)
    for key, value in amenity_json.items():
        setattr(got_obj, key, value)
    got_obj.save()
    return jsonify(got_obj.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_id(amenity_id):
    """
    Will delete an Amenity
    using id
    """

    got_obj = storage.get("Amenity", str(amenity_id))

    if got_obj is None:
        abort(404)

    storage.delet(got_obj)
    storage.save()

    return jsonify({})
