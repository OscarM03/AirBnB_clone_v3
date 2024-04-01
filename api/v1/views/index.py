#!/usr/bin/python3
"""routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    "status: ok"
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    "retrieves the number of each objects by type"
    my_dict = {}
    classes_list = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    names = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']

    for i in range(len(classes_list)):
        counts = storage.count(classes_list[i])
        my_dict[names[i]] = counts

    return jsonify(my_dict)
