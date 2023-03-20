"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import storage, templates
from app.utils.auth import get_username_for_page

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------

def _build_full_page_context(
  request: Request,
  username: str,
):
  reminder_lists = storage.get_lists(username)
  selected_list = storage.get_selected_reminders(username)

  return {
    'request': request,
    'username': username,
    'reminder_lists': reminder_lists,
    'selected_list': selected_list}


def _get_reminders_grid(request: Request, username: str):
  context = _build_full_page_context(request, username)
  return templates.TemplateResponse("partials/reminders/content.html", context)


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/reminders", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  context = _build_full_page_context(request, username)
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

@router.get("/reminders/list-row/{reminders_id}", response_class=HTMLResponse)
async def get_reminders_list_row(
  reminders_id: int,
  request: Request,
  username: str = Depends(get_username_for_page)
):
  reminder_list = storage.get_list(reminders_id, username)
  selected_list = storage.get_selected_reminders(username)
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row.html", context)


@router.delete("/reminders/list-row/{reminders_id}", response_class=HTMLResponse)
async def delete_reminders_list_row(
  reminders_id: int,
  request: Request,
  username: str = Depends(get_username_for_page)
):
  storage.delete_list(reminders_id, username)
  storage.reset_selected_after_delete(reminders_id, username)
  return _get_reminders_grid(request, username)


@router.patch("/reminders/list-row-name/{reminders_id}", response_class=HTMLResponse)
async def patch_reminders_list_row_name(
  reminders_id: int,
  request: Request,
  username: str = Depends(get_username_for_page),
  new_name: str = Form()
):
  storage.update_list_name(reminders_id, username, new_name)
  storage.set_selected_reminders(reminders_id, username)
  return _get_reminders_grid(request, username)


@router.get("/reminders/list-row-edit/{reminders_id}", response_class=HTMLResponse)
async def get_reminders_list_row_edit(
  reminders_id: int,
  request: Request,
  username: str = Depends(get_username_for_page)
):
  reminder_list = storage.get_list(reminders_id, username)
  selected_list = storage.get_selected_reminders(username)
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row-edit.html", context)


@router.get("/reminders/new-list-row", response_class=HTMLResponse)
async def get_reminders_new_list_row(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row.html", context)


@router.post("/reminders/new-list-row", response_class=HTMLResponse)
async def post_reminders_new_list_row(
  request: Request,
  username: str = Depends(get_username_for_page),
  reminder_list_name: str = Form()
):
  reminders_id = storage.create_list(reminder_list_name, username)
  storage.set_selected_reminders(reminders_id, username)
  return _get_reminders_grid(request, username)


@router.get("/reminders/new-list-row-edit", response_class=HTMLResponse)
async def get_reminders_new_list_row_edit(
  request: Request,
  username: str = Depends(get_username_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row-edit.html", context)


@router.post("/reminders/select/{reminders_id}", response_class=HTMLResponse)
async def post_reminders_select(
  reminders_id: int,
  request: Request,
  username: str = Depends(get_username_for_page)
):
  storage.set_selected_reminders(reminders_id, username)
  return _get_reminders_grid(request, username)
