#!/usr/bin/python3
"""
route for 
states objects
"""
from flask import jsonify, request, abort
from models.city import City
from api.v1.views import app_views, storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_state(state_id):
    """
    gets a city object 
    from a given state
    """
    ct_list=[]
    st_obj = storage.get("State", state_id)

    if st_obj is None:
        abort(404)
    for ob in st_obj.cities:
        ct_list.append(ob.to_json())

    return jsonify(ct_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_make(state_id):
    """
    Will create a route for 
    a city
    """
    ct_json = request.get_json(silent=True)
    if ct_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in ct_json:
        abort(400, 'Missing name')

    ct_json["state_id"] = state_id

    new_ct = City(**ct_json)
    new_ct.save()
    response = jsonify(new_ct.to_json())
    response.status_code = 201

    return response

@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def city_id(city_id):
    """
    Will get a city 
    object
    """

    got_obj = storage.get("City", str(city_id))

    if got_obj is None:
        abort(404)

    return jsonify(got_obj.to_json())


@app_views.route("cities/<city_id>", methods=["PUT"], 
                 strict_slashes=False)
def city_put(city_id):
    """
    Will update a city object
    using Id
    """
    ct_json = request.get_json(sitent=True)
    if ct_json is None:
        abort(400, "Not a JSON")
    got_obj = storage.get("City", str(city_id))
    if got_obj is None:
        abort(404)
    for key, value is ct_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setAttr(got_obj, key, value)
    got_obj.save()
    return jsonify(got_obj.to_json())

@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete_id(city_id):
    """
    Will deltes a city using 
    Id
    """
    got_bj = storage.get("City", str(city_id))

    if got_obj is None:
        abort(404)

    storage.delete(got_obj)
    storage.save()

    return jsonify({})
