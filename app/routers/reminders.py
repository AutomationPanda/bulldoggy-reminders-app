"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import get_storage_for_page
from app.utils.storage import ReminderStorage

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------

def _build_full_page_context(request: Request, storage: ReminderStorage):
  reminder_lists = storage.get_lists()
  selected_list = storage.get_selected_list()

  return {
    'request': request,
    'owner': storage.owner,
    'reminder_lists': reminder_lists,
    'selected_list': selected_list}


def _get_reminders_grid(request: Request, storage: ReminderStorage):
  context = _build_full_page_context(request, storage)
  return templates.TemplateResponse("partials/reminders/content.html", context)


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/reminders", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = _build_full_page_context(request, storage)
  return templates.TemplateResponse("pages/reminders.html", context)


@router.get("/reminders-frozen", summary="Logs into the app", response_class=HTMLResponse)
async def get_reminders(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request, 'owner': storage.owner}
  return templates.TemplateResponse("pages/reminders-frozen.html", context)


# --------------------------------------------------------------------------------
# Routes for list row partials
# --------------------------------------------------------------------------------

@router.get("/reminders/list-row/{list_id}", response_class=HTMLResponse)
async def get_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row.html", context)


@router.delete("/reminders/list-row/{list_id}", response_class=HTMLResponse)
async def delete_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.delete_list(list_id)
  storage.reset_selected_after_delete(list_id)
  return _get_reminders_grid(request, storage)


@router.patch("/reminders/list-row-name/{list_id}", response_class=HTMLResponse)
async def patch_reminders_list_row_name(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  new_name: str = Form()
):
  storage.update_list_name(list_id, new_name)
  storage.set_selected_list(list_id)
  return _get_reminders_grid(request, storage)


@router.get("/reminders/list-row-edit/{list_id}", response_class=HTMLResponse)
async def get_reminders_list_row_edit(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row-edit.html", context)


@router.get("/reminders/new-list-row", response_class=HTMLResponse)
async def get_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row.html", context)


@router.post("/reminders/new-list-row", response_class=HTMLResponse)
async def post_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  reminder_list_name: str = Form()
):
  list_id = storage.create_list(reminder_list_name)
  storage.set_selected_list(list_id)
  return _get_reminders_grid(request, storage)


@router.get("/reminders/new-list-row-edit", response_class=HTMLResponse)
async def get_reminders_new_list_row_edit(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row-edit.html", context)


@router.post("/reminders/select/{list_id}", response_class=HTMLResponse)
async def post_reminders_select(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.set_selected_list(list_id)
  return _get_reminders_grid(request, storage)


# --------------------------------------------------------------------------------
# Routes for item row partials
# --------------------------------------------------------------------------------

@router.get("/reminders/new-item-row", response_class=HTMLResponse)
async def get_reminders_new_item_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-item-row.html", context)


@router.post("/reminders/new-item-row", response_class=HTMLResponse)
async def post_reminders_new_item_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  reminder_item_name: str = Form()
):
  selected_list = storage.get_selected_list()
  storage.add_item(selected_list.id, reminder_item_name)
  return _get_reminders_grid(request, storage)


@router.get("/reminders/new-item-row-edit", response_class=HTMLResponse)
async def get_reminders_new_item_row_edit(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-item-row-edit.html", context)
