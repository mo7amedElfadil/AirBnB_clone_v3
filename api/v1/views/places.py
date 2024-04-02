#!/usr/bin/python3
"""
places: defining a blueprint view for Place object handling all
the default RESTful API actions

    /api/v1/places/<place_id> [GET, DELETE, PUT]
    /api/v1/citys/<city_id>/places [GET, POST]

"""

from flask.scaffold import F
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def get_place(place_id):
    """Returns an instance of place"""
    result = storage.get(Place, place_id)
    error_404(result)
    return jsonify(result.to_dict()), 200


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """Deletes an instance of place with the specific id"""
    result = storage.get(Place, place_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def put_place(place_id):
    """Updates an instance of the place entities"""
    result = storage.get(Place, place_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")

    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    for k, v in args.items():
        if k not in ["id", "user_id", "city_id",
                     "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """Returns a list of places with the specific city id"""
    result = storage.get(City, city_id)
    error_404(result)
    return jsonify([value.to_dict() for value in result.places]), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def post_place(city_id):
    """Adds a new instance of Place into the dataset"""
    result = storage.get(City, city_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    if not args.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, args["user_id"])
    if not user:
        abort(404)
    if not args.get("name"):
        abort(400, description="Missing name")
    args["city_id"] = city_id
    new_place = Place(**args)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def places_search():
    """
    retrieves all Place objects depending on the
    JSON in the body of the request.
    """
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    return jsonify(filter_places(**args)), 200


def filter_places(**kwargs):
    """ Filter place ids """
    city_ids = set()

    if "cities" in kwargs:
        city_ids.update(kwargs["cities"])
    if "states" in kwargs:
        for k_id in kwargs["states"]:
            state = storage.get(State, k_id)
            if not state:
                continue
            city_ids.update([city.id for city in state.cities])

    return exclude_places(retrieve_places(city_ids), **kwargs)


def exclude_places(places_set, **kwargs):
    """This function filters a list of places"""
    filtered_set = set()
    if "amenities" in kwargs:
        for place in places_set:
            am_ids = [amenity.id for amenity in place.amenities]
            if all(kw_id in am_ids for kw_id in kwargs["amenities"]):
                filtered_set.add(place)
        filtered_list = [place.to_dict() for place in filtered_set]
        for place in filtered_list:
            del place["amenities"]

        return filtered_list

    return [place.to_dict() for place in places_set]


def retrieve_places(city_list):
    """This function retrieves places"""
    places_set = set()
    places = storage.all(Place).values()
    for place in places:
        if place.city_id in city_list:
            places_set.add(place)
    return places_set
