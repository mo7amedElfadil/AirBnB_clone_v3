#!/usr/bin/python3
"""
states: defining a blueprint view for State object handling all
the default RESTful API actions

    /status: returns the status of the API
    /stats: returns the staticstis of the different entities
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"])
def get_states():
    """Returns a list of states"""
    return jsonify([value.to_dict() for value in storage.all(State).values()])


@app_views.route("/states", strict_slashes=False,
                 methods=["POST"])
def post_states():
    """Adds a new instance of State into the dataset"""
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    if not args.get("name"):
        abort(400, "Missing name")
    new_state = State(**args)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def get_state(state_id):
    """Returns a state with the specific id"""
    result = storage.get(State, state_id)
    error_404(result)
    return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Deletes an instance of state with the specific id"""
    result = storage.get(State, state_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def put_state(state_id):
    """Updates an instance of the state entities"""
    result = storage.get(State, state_id)
    error_404(result)
    if request.is_json is False or request.content_type != "application/json":
        abort(400, "Not a JSON")
    args = request.get_json(silent=True)
    for k, v in args.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(result, k, v)
    result.save()
    return jsonify(result.to_dict()), 200
