"""
This module provides security and authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import jwt
import secrets

from . import users, secret_key
from .exceptions import UnauthorizedException
from fastapi import Cookie, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

securityBasic = HTTPBasic(auto_error=False)


# --------------------------------------------------------------------------------
# Serializers
# --------------------------------------------------------------------------------

def serialize_token(username: str):
  return jwt.encode({"username": username}, secret_key, algorithm="HS256")


def deserialize_token(token: str):
  try:
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
    return data['username']
  except:
    return None


# --------------------------------------------------------------------------------
# Authentication Checkers
# --------------------------------------------------------------------------------

def get_http_basic_username(basic: HTTPBasicCredentials = Depends(securityBasic)):
  if basic.username in users:
    if secrets.compare_digest(basic.password, users[basic.username]):
      return basic.username

  raise UnauthorizedException()


def get_auth_cookie_username(session: str | None = Cookie(default=None)):
  if session and session in users:
    return session

  raise UnauthorizedException()
