#!/usr/bin/python3
"""
users: defining a blueprint view for User object handling all
the default RESTful API actions

    /status: returns the status of the API
    /stats: returns the staticstis of the different entities

"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def get_user(user_id):
    """Returns a user with the specific id"""
    result = storage.get(User, user_id)
    error_404(result)
    return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """Deletes an instance of user with the specific id"""
    result = storage.get(User, user_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def put_user(user_id):
    """Updates an instance of the user entities"""
    result = storage.get(User, user_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    for k, v in args.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200


@app_views.route("/users", strict_slashes=False,
                 methods=["GET"])
def get_users():
    """Returns a list of users"""
    return jsonify([value.to_dict() for value in
                    storage.all(User).values()])


@app_views.route("/users", strict_slashes=False,
                 methods=["POST"])
def post_new_user():
    """Adds a new instance of User into the dataset"""
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args.get("email"):
        abort(400, "Missing email")
    if not args.get("password"):
        abort(400, "Missing password")
    new_user = User(**args)
    new_user.save()
    return jsonify(new_user.to_dict()), 201
