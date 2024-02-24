#!/usr/bin/python3
"""
Handles state object
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_acq_all():
    """
    gets state objects
    """
    state_ls = []
    state_obj = storage.all("State")
    for ob in state_obj.values():
        state_ls.append(ob.to_json())

    return jsonify(state_ls)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_make():
    """
    will create a state
    route
    """
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, 'Not a JSON')
    if "name" not in st_json:
        abort(400, 'Missing name')

    new_state = State(**st_json)
    new_state.save()
    response = jsonify(new_state.to_json())
    response.status_code = 201

    return response


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_get_id(state_id):
    """
    Will get a specific object id for
    a state
    """
    got_obj = storage.get("State", str(state_id))

    if got_obj is None:
        abort(404)

    return jsonify(got_obj.to_json())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put_id(state_id):
    """
    Will update States object
    using id
    """
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, "Not a JSON")
    got_obj = storage.get("State", str(stae_id))
    if got_obj is None:
        abort(404)
    for key, value in st_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(got_obj, key, value)
    got_obj.save()
    return jsonify(got_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_id(state_id):
    """
    Deletes states, using
    id
    """

    got_obj = storage.get("State", str(state_id))

    if got_obj is None:
        abort(404)

    storage.delete(got_obj)
    storage.save()

    return jsonify({})
