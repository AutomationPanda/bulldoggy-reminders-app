"""
This module provides routes for authentication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import AuthCookie, get_login_form_creds, get_auth_cookie

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/login", summary="Gets the login page", response_class=HTMLResponse)
async def get_login(request: Request):
  return templates.TemplateResponse("login.html", {'request': request})


@router.post("/login", summary="Logs into the app")
async def post_login(cookie: AuthCookie = Depends(get_login_form_creds)) -> dict:
  response = RedirectResponse('/reminders', status_code=302)
  response.set_cookie(key=cookie.name, value=cookie.token)
  return response


@router.post("/logout", summary="Logs out of the app")
async def post_login(response: Response, cookie: AuthCookie = Depends(get_auth_cookie)) -> dict:
  response.set_cookie(key=cookie.name, value=cookie.token, expires=-1)
  return {"message": f"Logged out as {cookie.username}"}
