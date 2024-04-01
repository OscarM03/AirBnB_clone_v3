#!/usr/bin/python3
"""Getting states"""
from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states',
                 methods=['GET'], strict_slashes=False)
def get_states():
    """"Get states"""
    states = storage.all(State).values()

    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def create_state():
    """creatre a new state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    new_obj = State(**data)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
