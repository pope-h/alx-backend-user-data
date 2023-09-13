#!/usr/bin/env python3
"""
This script defines the routes for the API and handles authentication.

The following functions are defined in this script:

* `not_found()` - This function handles 404 errors.
* `unauthorized()` - This function handles 401 errors.
* `forbidden()` - This function handles 403 errors.
* `before_request()` - function checks for authentication before every request.

The following variables are defined in this script:

* `app` - The Flask app object.
* `auth` - The authentication object.
* `authorized_list` - A list of paths that do not require authentication.

"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler

    Args:
        error (Exception): The error that was raised.

    Returns:
        str: The JSON response that is returned to the client.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler

    Args:
        error (Exception): The error that was raised.

    Returns:
        str: The JSON response that is returned to the client.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ forbidden handler

    Args:
        error (Exception): The error that was raised.

    Returns:
        str: The JSON response that is returned to the client.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    handler before_request

    Checks for authentication before every request.
    If the request requires authentication and the user is not authenticated,
    the function aborts the request with a 401 error.
    """
    authorized_list = ['/api/v1/status/',
                       '/api/v1/unauthorized/',
                       '/api/v1/forbidden/',
                       '/api/v1/auth_session/login/']

    if auth and auth.require_auth(request.path, authorized_list):
        if auth.authorization_header(request) is None \
                and auth.session_cookie(request) is None:
            abort(401)
        if auth.authorization_header(request) \
                and auth.session_cookie(request) is None:
            abort(401)
        if not auth.current_user(request):
            abort(403)
        request.current_user = auth.current_user(request)
        if auth.authorization_header(request) \
                and auth.session_cookie(request) is None:
            abort(401)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
