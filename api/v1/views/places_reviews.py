#!/usr/bin/python3
from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place 
from models.user import User

@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_from_places(place_id):
    """"Get reviews from certain places"""
    place = storage.get(Place, place_id)
    reviews = []

    if place is None:
        abort(404)
    else:
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
    """Get reviews"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """creatre a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    if 'text' not in data:
        abort(400, "Missing text")
    
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_obj = Review(**data)
    new_obj.place_id = place_id
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
