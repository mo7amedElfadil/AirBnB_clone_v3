#!/usr/bin/python3
"""
places_reviews: defining a blueprint view for Review object handling all
the default RESTful API actions

    /api/v1/places/<place_id>/amenities
    [GET]

    /api/v1/places/<place_id>/amenities/<amenity_id>
    [DELETE, POST]

"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def get_place_amenities(place_id):
    """Returns a list of amenities for a certain place"""
    place = storage.get(Place, place_id)
    error_404(place)

    # Checking if amenity is linked to place according to storage
    if getenv("HBNB_TYPE_STORAGE") == "db":
        return jsonify([value.to_dict() for value in place.amenities])
    else:
        return jsonify([storage.get(Amenity, id_).to_dict()
                        for id_ in place.amenity_ids])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity object that is linked to a certain place"""
    place = storage.get(Place, place_id)
    error_404(place)
    amenity = storage.get(Amenity, amenity_id)
    error_404(amenity)

    # Checking if amenity is linked to place according to storage
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)

    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def add_place_amenity(place_id, amenity_id):
    """Adds a new amenity object to a place"""
    place = storage.get(Place, place_id)
    error_404(place)
    amenity = storage.get(Amenity, amenity_id)
    error_404(amenity)

    # Checking if amenity is linked to place according to storage
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)

    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
