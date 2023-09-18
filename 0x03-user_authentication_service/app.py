#!/usr/bin/env python3
""" Flask app """

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """home route view
    """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """user registration app
    """
    user_email = request.form.get('email')
    password = request.form.get('password')
    try:
        if AUTH.register_user(user_email, password):
            response = {"email": user_email, "message": "user created"}
            return jsonify(response), 200
        return
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
