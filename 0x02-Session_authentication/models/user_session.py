#!/usr/bin/env python3
""" user session model """
from models.base import Base


class UserSession(Base):
    """ session module """

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
