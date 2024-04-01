#!/usr/bin/python3
"""
places_reviews: defining a blueprint view for Review object handling all
the default RESTful API actions

    /api/v1/places/<place_id>/reviews [GET, POST]
    /api/v1/reviews/<review_id> [GET, DELETE, PUT]

"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """Returns a list of reviews for a certain place"""
    result = storage.get(Place, place_id)
    error_404(result)
    return jsonify([value.to_dict() for value in result.reviews]), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    """Returns a review with the specific state id"""
    result = storage.get(Review, review_id)
    error_404(result)
    return jsonify(result.to_dict()), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """Deletes an instance of review with the specific id"""
    result = storage.get(Review, review_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def post_new_review(place_id):
    """Adds a new instance of Review into the dataset"""
    result = storage.get(Place, place_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    if not args.get("user_id"):
        abort(400, "Missing user_id")
    if not storage.get(User, args["user_id"]):
        abort(404)
    if not args.get("text"):
        abort(400, "Missing text")
    new_review = Review(**args)
    new_review.save()
    result.reviews.append(new_review)
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def put_review(review_id):
    """Updates an instance of the review entities"""
    result = storage.get(Review, review_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    for k, v in args.items():
        if k not in ["id", "user_id", "place_id",
                     "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200
