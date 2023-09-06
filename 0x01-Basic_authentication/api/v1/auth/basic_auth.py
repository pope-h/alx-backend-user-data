#!/usr/bin/env python3
"""
Basic Auth module
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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
        u_email, u_password = decoded_base64_authorization_header.split(':', 1)
        return u_email, u_password
