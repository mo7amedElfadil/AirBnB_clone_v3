#!/usr/bin/python3
"""
amenities: defining a blueprint view for Amenity object handling all
the default RESTful API actions

    /api/v1/amenities [GET, POST]
    /api/v1/amenities/<amenity_id> [DELETE, GET, PUT]
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """Returns an instance of amenity"""
    result = storage.get(Amenity, amenity_id)
    error_404(result)
    return jsonify(result.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an instance of amenity with the specific id"""
    result = storage.get(Amenity, amenity_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def put_amenity(amenity_id):
    """Updates an instance of the amenity entities"""
    result = storage.get(Amenity, amenity_id)
    error_404(result)
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    for k, v in args.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"])
def get_all_amenities():
    """Returns a list of all amenities"""
    result = storage.all(Amenity)
    return jsonify([value.to_dict() for value in result.values()])


@app_views.route("/amenities", strict_slashes=False,
                 methods=["POST"])
def post_new_amenity():
    """Adds a new instance of Amenity into the dataset"""
    args = request.get_json(silent=True)
    if not args:
        abort(400, "Not a JSON")
    if not args.get("name"):
        abort(400, "Missing name")
    new_amenity = Amenity(**args)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201
