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

router = APIRouter(prefix="/reminders")


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

@router.get(
  path="",
  summary="Gets the reminders page",
  tags=["Pages"],
  response_class=HTMLResponse
)
async def get_reminders(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = _build_full_page_context(request, storage)
  return templates.TemplateResponse("pages/reminders.html", context)


# --------------------------------------------------------------------------------
# Routes for list row partials
# --------------------------------------------------------------------------------

@router.get(
  path="/list-row/{list_id}",
  summary="Partial: Gets a reminder list row by ID",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row.html", context)


@router.delete(
  path="/list-row/{list_id}",
  summary="Partial: Deletes a reminder list row",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def delete_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.delete_list(list_id)
  storage.reset_selected_after_delete(list_id)
  return _get_reminders_grid(request, storage)


@router.patch(
  path="/list-row-name/{list_id}",
  summary="Partial: Updates a reminder list row's name",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def patch_reminders_list_row_name(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  new_name: str = Form()
):
  storage.update_list_name(list_id, new_name)
  storage.set_selected_list(list_id)
  return _get_reminders_grid(request, storage)


@router.get(
  path="/list-row-edit/{list_id}",
  summary="Partial: Changes a reminder list row into editing mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_list_row_edit(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()
  context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
  return templates.TemplateResponse("partials/reminders/list-row-edit.html", context)


@router.get(
  path="/new-list-row",
  summary="Partial: Gets the row for adding a new reminder list",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row.html", context)


@router.post(
  path="/new-list-row",
  summary="Partial: Creates a new reminder list",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def post_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  reminder_list_name: str = Form()
):
  list_id = storage.create_list(reminder_list_name)
  storage.set_selected_list(list_id)
  return _get_reminders_grid(request, storage)


@router.get(
  path="/new-list-row-edit",
  summary="Partial: Changes the new reminder list row into editing mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_list_row_edit(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-list-row-edit.html", context)


@router.post(
  path="/select/{list_id}",
  summary="Partial: Selects a new reminder list row",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
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

@router.get(
  path="/item-row/{item_id}",
  summary="Partial: Gets a new reminder item row by ID",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_item_row(
  item_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_item = storage.get_item(item_id)
  context = {'request': request, 'reminder_item': reminder_item}
  return templates.TemplateResponse("partials/reminders/item-row.html", context)


@router.delete(
  path="/item-row/{item_id}",
  summary="Partial: Deletes a new reminder item row",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def delete_reminders_item_row(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.delete_item(item_id)
  return ""


@router.patch(
  path="/item-row-description/{item_id}",
  summary="Partial: Updates a reminder item row's description",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def patch_reminders_item_row_description(
  item_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  new_description: str = Form()
):
  storage.update_item_description(item_id, new_description)
  reminder_item = storage.get_item(item_id)
  context = {'request': request, 'reminder_item': reminder_item}
  return templates.TemplateResponse("partials/reminders/item-row.html", context)


@router.patch(
  path="/item-row-strike/{item_id}",
  summary="Partial: Toggles a reminder item's completed status",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def patch_reminders_item_row_strike(
  item_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.strike_item(item_id)
  reminder_item = storage.get_item(item_id)
  context = {'request': request, 'reminder_item': reminder_item}
  return templates.TemplateResponse("partials/reminders/item-row.html", context)


@router.get(
  path="/item-row-edit/{item_id}",
  summary="Partial: Changes a reminder item row into editing mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_item_row_edit(
  item_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_item = storage.get_item(item_id)
  context = {'request': request, 'reminder_item': reminder_item}
  return templates.TemplateResponse("partials/reminders/item-row-edit.html", context)


@router.get(
  path="/new-item-row",
  summary="Partial: Gets the new reminder item row",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_item_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-item-row.html", context)


@router.post(
  path="/new-item-row",
  summary="Partial: Creates a new reminder item in the selected list",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def post_reminders_new_item_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  reminder_item_name: str = Form()
):
  selected_list = storage.get_selected_list()
  storage.add_item(selected_list.id, reminder_item_name)
  return _get_reminders_grid(request, storage)


@router.get(
  path="/new-item-row-edit",
  summary="Partial: Changes the new reminder item row into edit mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_item_row_edit(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}
  return templates.TemplateResponse("partials/reminders/new-item-row-edit.html", context)
