#!/usr/bin/env python3
"""definition of class Auth"""
from flask import request
from typing import TypeVar, List
import os


class Auth:
    """class to manage api authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if authentication is required for the given path."""
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    
    def authorization_header(self, request=None) -> str:
        """returns None"""
        if request is None:
            return None
        if 'Authorization' not in request.keys():
            return None
        else:
            return request['Authorization']
    
    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """returns None"""
        return None
    
    def session_cookies(self, request=None):
        """gets a cookie value"""
        if request is None:
            return None
        session = os.getenv('SESSION_NAME')
        if session == '_my_session_id':
            cookie_value = request.cookies.get(session)
            return cookie_value
        
        return None
    