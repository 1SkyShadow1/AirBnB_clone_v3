#!/usr/bin/python3
"""
route for handling place
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places>", methods=["GET"],
                 strict_slashes=False)
def place_city(city_id):
    """"
    retrieves all place objects
    :return: json all places
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    for obj in city_obj.places:
        place_list.append(obj.to_json())

    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_make(city_id):
    """
    create place
    :return: newly created place obj
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def place_id(place_id):
    """
    gets place object by ID
    :param place_id: place obj id
    :return: place obj with specified id or error
    """

    fetched_obj = storage.get("Place", str(place_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    updates specific Plce obj by ID
    :param place_id: place obj ID
    :return: PLace obj and 200 on success or 400 or 404 on fail
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("Place", str(place_id))

    if fetched_obj is None:
        abort(404)

    for key, val in place_json.item():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete_id(place_id):
    """
    deletes Place by id
    :param pla_id: PLace object id
    :return: empty dict with 200 or 404 not found
    """

    fetched_obj = storage.get("Place", str(place_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
