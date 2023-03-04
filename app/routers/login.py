"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from ..auth import *

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class UserAccount(BaseModel):
  username: str
  password: str


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.post("/login", summary="Logs into the app")
async def post_login(response: Response, user_token: UserToken = Depends(get_http_basic_token)) -> dict():
  response.set_cookie(key=auth_cookie, value=user_token.token)
  return {"message": f"Logged in as {user_token.username}"}


@router.post("/logout", summary="Logs out of the app")
async def post_login(response: Response, user_token: UserToken = Depends(get_auth_cookie_token)) -> dict():
  response.set_cookie(key=auth_cookie, value=user_token.token, expires=-1)
  return {"message": f"Logged out as {user_token.username}"}
