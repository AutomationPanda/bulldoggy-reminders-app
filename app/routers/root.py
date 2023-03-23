"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import AuthCookie, get_auth_cookie

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from typing import Optional


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get(
  path="/",
  summary="Redirects to the login or reminders pages",
  tags=["Pages"]
)
async def read_root(
  cookie: Optional[AuthCookie] = Depends(get_auth_cookie)
):
  path = '/reminders' if cookie else '/login'
  return RedirectResponse(path, status_code=302)


@router.get(
  path="/favicon.ico",
  include_in_schema=False
)
async def get_favicon():
  return FileResponse("static/img/favicon.ico")


@router.get(
  path="/not-found",
  summary="Gets the \"Not Found\" page",
  tags=["Pages"]
)
async def get_not_found(
  request: Request
):
  return templates.TemplateResponse("pages/not-found.html", {'request': request})
