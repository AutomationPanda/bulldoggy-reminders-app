"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .. import db, users
from ..auth import get_http_basic_username, get_auth_cookie_username

from fastapi import APIRouter, Cookie, Depends, Response
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
async def post_login(response: Response, username: str = Depends(get_http_basic_username)) -> dict():
  response.set_cookie(key="session", value=username)
  return {"message": f"Logged in as {username}"}


@router.post("/logout", summary="Logs out of the app")
async def post_login(response: Response, username: str = Depends(get_auth_cookie_username)) -> dict():
  response.set_cookie(key="session", value=username, expires=-1)
  return {"message": f"Logged out as {username}"}


@router.get("/items")
async def read_items(username: str = Depends(get_auth_cookie_username)) -> dict:
  return {"session": username}
