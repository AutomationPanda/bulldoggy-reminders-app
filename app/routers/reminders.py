"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates, table
from app.utils.auth import get_username_for_page

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/reminders", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  reminder_lists = table.get_lists(username)
  context = {'request': request, 'username': username, 'reminder_lists': reminder_lists}
  return templates.TemplateResponse("pages/reminders.html", context)


@router.get("/reminders-frozen", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  context = {'request': request, 'username': username}
  return templates.TemplateResponse("pages/reminders-frozen.html", context)


# --------------------------------------------------------------------------------
# Routes for partials
# --------------------------------------------------------------------------------

@router.get("/reminders/new-list-row", response_class=HTMLResponse)
async def get_reminders_new_list_row(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  return templates.TemplateResponse("partials/reminders/new-list-row.html", {'request': request})


@router.get("/reminders/new-list-row-edit", response_class=HTMLResponse)
async def get_reminders_new_list_row_input(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  return templates.TemplateResponse("partials/reminders/new-list-row-edit.html", {'request': request})


@router.post("/reminders/new-list-row-added", response_class=HTMLResponse)
async def post_reminders_new_list_row_added(
  request: Request,
  username: str = Depends(get_username_for_page),
  list_name: str = Form()
):
  context = {'request': request, 'list_name': list_name}
  return templates.TemplateResponse("partials/reminders/new-list-row-added.html", context)


@router.delete("/reminders/list-row", response_class=HTMLResponse)
async def post_reminders_new_list_row_added(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  return ""
