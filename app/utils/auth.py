"""
This module provides security and authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import jwt
import secrets

from app import users, secret_key
from app.utils.exceptions import UnauthorizedException

from fastapi import Cookie, Form
from fastapi.security import HTTPBasic
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------

basic_auth = HTTPBasic(auto_error=False)
auth_cookie_name = "reminders_session"


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class AuthCookie(BaseModel):
  name: str
  token: str
  username: str


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

def get_login_form_creds(username: str = Form(), password: str = Form()) -> AuthCookie:
  if username in users:
    if secrets.compare_digest(password, users[username]):
      token = serialize_token(username)
      return AuthCookie(
        name=auth_cookie_name,
        username=username,
        token=token)

  return None


def get_auth_cookie(reminders_session: str | None = Cookie(default=None)) -> AuthCookie:
  if reminders_session:
    username = deserialize_token(reminders_session)
    if username and username in users:
      return AuthCookie(
        name=auth_cookie_name,
        username=username,
        token=reminders_session)

  raise UnauthorizedException()
