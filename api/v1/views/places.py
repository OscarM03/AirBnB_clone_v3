#!/usr/bin/python3
"""Getting places"""
from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_in_cities(city_id):
    """"Get places for a specific city"""
    city = storage.get(City, city_id)
    places_list = []

    if city is None:
        abort(404)
    else:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creatre a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing name")

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_obj = Place(**data)
    new_obj.city_id = city_id
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
