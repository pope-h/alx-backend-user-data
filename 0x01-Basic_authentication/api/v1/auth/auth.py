#!/usr/bin/env python3
""" Auth Class """

from flask import request
from typing import List, TypeVar


class Auth():
    """
    a class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
