#!/usr/bin/env python3
"""
Basic Auth module
"""
import base64
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from flask import request


class BasicAuth(Auth):
    """
    class BasicAuth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
         returns the Base64 part of the Authorization
         header for a Basic Authentication
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a
        Base64 string base64_authorization_header
        """
        b64AH = base64_authorization_header
        if (b64AH is None or not isinstance(b64AH, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(b64AH)
        except (TypeError, binascii.Error):
            return None
        decoded_strings = decoded_bytes.decode('utf-8')
        return decoded_strings

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ":" not in decoded_base64_authorization_header):
            return None, None
        user_email, user_pwd = decoded_base64_authorization_header \
            .split(':', 1)
        return user_email, user_pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if (user_email is None or not isinstance(user_email, str) or
                user_pwd is None or not isinstance(user_pwd, str)):
            return None
        users = User.search({"email": user_email})
        if users is None:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        # If the password is not valid, return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64header)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_creds)
