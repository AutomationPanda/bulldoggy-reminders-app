"""
This module provides routes for the API.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.auth import get_storage_for_api
from app.utils.storage import ReminderList, ReminderStorage

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/api")


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class NewReminderListName(BaseModel):
  name: str


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get(
  path="/reminders",
  summary="Get the user's reminder lists",
  response_model=List[ReminderList]
)
async def get_reminders(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> list[ReminderList]:
  """Gets the list of all reminder lists owned by the user."""

  return storage.get_lists()


@router.post(
  path="/reminders",
  summary="Create a new reminder list",
  response_model=ReminderList
)
async def post_reminders(
  reminder_list: NewReminderListName,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:
  """Creates a new reminder list for the user."""

  list_id = storage.create_list(reminder_list.name)
  return storage.get_list(list_id)


@router.get(
  path="/reminders/{list_id}",
  summary="Get a reminder list by ID",
  response_model=ReminderList
)
async def get_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:
  """Gets a reminder list by ID."""

  return storage.get_list(list_id)


@router.patch(
  path="/reminders/{list_id}",
  summary="Updates a reminder list's name",
  response_model=ReminderList
)
async def patch_list_id(
  list_id: int,
  reminder_list: NewReminderListName,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:
  """Updates a reminder list's name."""
  
  storage.update_list_name(list_id, reminder_list.name)
  return storage.get_list(list_id)


@router.delete(
  path="/reminders/{list_id}",
  summary="Deletes a reminder list",
  response_model=dict
)
async def delete_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> dict:
  """Deletes the reminder list by ID."""

  storage.delete_list(list_id)
  return dict()
