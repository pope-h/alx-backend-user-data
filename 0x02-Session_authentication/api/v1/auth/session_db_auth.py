#!/usr/bin/env python3
""" Storage class for authentication """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from api.v1.app import auth


class SessionDBAuth(SessionExpAuth):
    """ Session Authentication Class with Database """
    def create_session(self, user_id=None):
        """ Create a Session ID and store it in the database """
        session_id = super().create_session((user_id))
        if session_id is not None:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve User ID for Session ID from the database """
        if session_id is None:
            return None
            user_session = UserSession.search({'session_id': session_id})
            if user_session:
                return user_session[0].user_id
            return None

    def destroy_session(self, request=None):
        """ Destroy UserSession based on Session ID from request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
