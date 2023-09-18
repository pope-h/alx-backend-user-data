#!/usr/bin/env python3
""" Flask app """

from flask import Flask, jsonify, request, abort, redirect
from user import User
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ User login app
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Log user out
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ returns user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)

    if not user:
        abort(403)
    email = user.email
    payload = {"email": email}
    return jsonify(payload), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get reset token
    """
    email = request.form.get('email')
    user_session_id = AUTH.create_session(email)

    if not user_session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id=user_session_id)
    if not user:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    payload = {"email": email, "reset_token": token}
    return jsonify(payload), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Password update app
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        payload = {"email": email, "message": "Password updated"}
        return jsonify(payload), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
