#!/usr/bin/env python3
""" Auth Class """

from typing import List, TypeVar
from flask import request


class Auth():
    """
    a class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks path for auth """
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path.rstrip('*')):
                    return False
            elif path == excluded_path:
                return False
        if path[-1] != '/':
            check += '/'
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None """
        if request is None:
            return None
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None
        return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
