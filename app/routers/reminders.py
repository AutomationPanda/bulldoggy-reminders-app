"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import AuthCookie, get_auth_cookie

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/reminders", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(request: Request, cookie: AuthCookie = Depends(get_auth_cookie)):
  return templates.TemplateResponse("reminders.html", {'request': request})
