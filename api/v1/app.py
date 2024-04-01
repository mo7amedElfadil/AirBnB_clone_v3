#!/usr/bin/python3
"""
Flask web api
methods: GET, POST, PUT, DELETE
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSON_SORT_KEYS'] = True
# app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(_):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(_):
    """Return 404 error"""
    return {"error": "Not found"}, 404


@app.errorhandler(400)
def bad_request(_):
    """Return 400 error"""
    return _.description, 400


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", 5000)),
            threaded=True)
