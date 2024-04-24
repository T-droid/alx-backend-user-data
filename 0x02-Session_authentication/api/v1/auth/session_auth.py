#!/usr/bin/env python3
"""implimenting session authentification"""

from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """session authentification mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        sesh_id = uuid.uuid4()
        self.user_id_by_session_id[str(sesh_id)] = user_id
        return str(sesh_id)
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """gets user id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
    