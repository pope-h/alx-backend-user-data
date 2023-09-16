#!/usr/bin/env python3
""" Auth Module """


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments
    and returns bytes
    """
    bytePwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashPwd = bcrypt.hashpw(bytePwd, salt)

    return hashPwd
