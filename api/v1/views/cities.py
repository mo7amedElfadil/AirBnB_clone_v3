#!/usr/bin/python3
"""
cities: defining a blueprint view for City object handling all
the default RESTful API actions

    /api/v1/cities/<city_id> [GET, DELETE, PUT]
    /api/v1/states/<state_id>/cities [GET, POST]

"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["GET"])
def get_city(city_id):
    """Returns an instance of city"""
    result = storage.get(City, city_id)
    error_404(result)
    return jsonify(result.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_city(city_id):
    """Deletes an instance of city with the specific id"""
    result = storage.get(City, city_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def put_city(city_id):
    """Updates an instance of the city entities"""
    result = storage.get(City, city_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    for k, v in args.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """Returns a list of cities with the specific state id"""
    result = storage.get(State, state_id)
    error_404(result)
    return jsonify([value.to_dict() for value in result.cities])


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def post_new_city(state_id):
    """Adds a new instance of City into the dataset"""
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args.get("name"):
        abort(400, "Missing name")
    result = storage.get(State, state_id)
    error_404(result)
    args["state_id"] = state_id
    new_city = City(**args)
    new_city.save()
    return jsonify(new_city.to_dict()), 201
