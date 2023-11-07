#!/usr/bin/env python3
""" A BasicAuth class that inherits from Auth """

from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            item = base64_authorization_header.encode('utf-8')
            decoded_item = base64.b64decode(item)
            return decoded_item.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        for u in user:
            if u.is_valid_password(user_pwd):
                return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_hdr = self.extract_base64_authorization_header(auth_header)
        if base64_hdr is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_hdr)
        if decoded_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_header)
        if user_credentials is None:
            return None
        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
        return user
