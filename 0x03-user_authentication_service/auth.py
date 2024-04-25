#!/usr/bin/env python3
"""authorisation of user"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import uuid


def _hash_password(pwd: str) -> bytes:
    """encryptes a password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generates new uuids"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers new user"""
        if email is None or password is None:
            return None
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        
    def valid_login(self, email: str, password: str) ->bool:
        """validates user logins"""
        try:
            login_user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), login_user.hashed_password):
                return True
            return False
        
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a user session"""
        try:
            user = self._db.find_user_by(email=email)
            sesh_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sesh_id)
            return sesh_id
        except NoResultFound:
            return None
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """checks if user has a session"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
    
    def get_reset_password_token(self, email: str) -> str:
        """gets user reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    
    def destroy_session(self, user_id: int) -> None:
        """closses a user session"""
        self._db.update_user(user_id, session_id=None)
