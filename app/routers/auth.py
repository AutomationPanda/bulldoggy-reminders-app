"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .. import db, users

from fastapi import APIRouter, Cookie, Response
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
async def post_login(user: UserAccount, response: Response) -> dict():
  response.set_cookie(key="session", value=user.username)
  return {"message": f"Logged in as {user.username}"}


@router.post("/logout", summary="Logs out of the app")
async def post_login(response: Response, session: str | None = Cookie(default=None)) -> dict():
  response.set_cookie(key="session", value=session, expires=-1)
  return {"message": f"Logged out as {session}"}


# @router.get("/items")
# async def read_items(session: str | None = Cookie(default=None)) -> dict:
#   return {"session": session}
