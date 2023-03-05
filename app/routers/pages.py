"""
This module provides routes for web pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/login", summary="Gets the login page", response_class=HTMLResponse)
async def get_login(request: Request):
  return templates.TemplateResponse("login.html", {'request': request})
