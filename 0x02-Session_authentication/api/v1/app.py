#!/usr/bin/env python3
"""
    Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request, Blueprint
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = getenv("AUTH_TYPE")
auth = None


@app.before_request
def auth():
    """ Path authenticator
    """
    excluded = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']
    # auth = getenv("AUTH_TYPE")

    if auth and auth == 'auth':
        auth = Auth()
    elif auth == 'basic_auth':
        auth = BasicAuth()
    elif auth == 'session_auth':
        auth = SessionAuth()
    elif auth is None:
        return

    if not auth.require_auth(request.path, excluded):
        return
    elif not auth.authorization_header(request) and\
            not auth.session_cookie(request):
        return abort(401)
    elif auth.current_user(request) is None:
        return abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
