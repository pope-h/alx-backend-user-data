#!/usr/bin/env python3
"""
class to add an expiration date to a Session ID
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from typing import TypeVar


class SessionExpAuth(SessionAuth):
    """ Session Expired Authentication Class """
    def __init__(self):
        """ Initialize SessionExpAuth """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ Create a Session ID with expiration date """
        session_id = super().create_session(user_id)
        if session_id is not None:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve User ID for Session ID """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict['created_at']
        session_expiry = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() <= session_expiry:
            return session_dict['user_id']

        return None
