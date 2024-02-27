#!/usr/bin/python3
"""
This module contains Flask views for
index-related routes

It includes two routes:
    - /status: Returns a JSON response indicating the status
    - /stats: Return a Json response containing statistics for objects
"""
# importing necessary modules
from flask import jsonify
from api.v1.views import app_views
from models import storage

# method to display json response for status


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route

    Return:
        Response: JSON response indicating the status
    """
    data = {
            "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp

# method for displaying json response for all objs


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Stats route

    Return:
        Response: JSON response  of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
