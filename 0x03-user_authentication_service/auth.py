#!/usr/bin/env python3
""" Auth Module """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments
    and returns bytes
    """
    bytePwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashPwd = bcrypt.hashpw(bytePwd, salt)

    return hashPwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        User registration method
        """
        db = self._db

        try:
            user = db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            pwd = _hash_password(password)
            user = db.add_user(email, pwd)

            return user