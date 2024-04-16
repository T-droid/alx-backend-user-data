#!/usr/bin/python3
"""definition of basic auth"""
from api.v1.auth.auth import Auth
import base64
import binascii


class BasicAuth(Auth):
    """implimentation of basic auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorisation"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len("Basic "):]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """used to decode value using base64"""
        b64_auth_header = base64_authorization_header
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encode = b64_auth_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None
            
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str): # type: ignore
        """extracts user password and email"""
        if (decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ':' not in decoded_base64_authorization_header):
            return (None, None)
        user_credentials = tuple(decoded_base64_authorization_header.split(':'))
        return user_credentials
        