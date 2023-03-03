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
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

auth_cookie = "reminders_session"
basic_auth = HTTPBasic(auto_error=False)


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class UserToken(BaseModel):
  username: str
  token: str


# --------------------------------------------------------------------------------
# Serializers
# --------------------------------------------------------------------------------

def serialize_token(username: str) -> str:
  return jwt.encode({"username": username}, secret_key, algorithm="HS256")


def deserialize_token(token: str) -> str:
  try:
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
    return data['username']
  except:
    return None


# --------------------------------------------------------------------------------
# Authentication Checkers
# --------------------------------------------------------------------------------

def get_http_basic_token(basic: HTTPBasicCredentials = Depends(basic_auth)) -> UserToken:
  if basic.username in users:
    if secrets.compare_digest(basic.password, users[basic.username]):
      token = serialize_token(basic.username)
      return UserToken(username=basic.username, token=token)

  raise UnauthorizedException()


def get_auth_cookie_token(reminders_session: str | None = Cookie(default=None)) -> str:
  if reminders_session:
    username = deserialize_token(reminders_session)
    if username and username in users:
      return UserToken(username=username, token=reminders_session)

  raise UnauthorizedException()
