"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import get_username_for_page

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
async def get_reminders(request: Request, username: str = Depends(get_username_for_page)):
  return templates.TemplateResponse("pages/reminders.html", {'request': request, 'username': username})


@router.get("/reminders-frozen", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(request: Request, username: str = Depends(get_username_for_page)):
  return templates.TemplateResponse("pages/reminders-frozen.html", {'request': request, 'username': username})


# --------------------------------------------------------------------------------
# Routes for partials
# --------------------------------------------------------------------------------

@router.get("/reminders/new-list-row", response_class=HTMLResponse)
async def get_reminders_new_list_row(request: Request, username: str = Depends(get_username_for_page)):
  return templates.TemplateResponse("partials/reminders/new-list-row.html", {'request': request})


@router.get("/reminders/new-list-row-input", response_class=HTMLResponse)
async def get_reminders_new_list_row_input(request: Request, username: str = Depends(get_username_for_page)):
  return templates.TemplateResponse("partials/reminders/new-list-row-input.html", {'request': request})
