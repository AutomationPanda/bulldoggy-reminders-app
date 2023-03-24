"""
This module provides routes for the API,
which provides a "backdoor" for reminder data management.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.auth import get_storage_for_api
from app.utils.storage import ReminderList, ReminderItem, ReminderStorage

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(
  prefix="/api",
  tags=["API"]
)


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class NewReminderListName(BaseModel):
  name: str


class NewReminderItem(BaseModel):
  description: str


class SelectedListId(BaseModel):
  list_id: Optional[int]


# --------------------------------------------------------------------------------
# Routes for reminder lists
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
) -> Dict:
  """Deletes a reminder list by ID."""

  storage.delete_list(list_id)
  return dict()


# --------------------------------------------------------------------------------
# Routes for reminder items
# --------------------------------------------------------------------------------

@router.get(
  path="/reminders/{list_id}/items",
  summary="Get all reminder items for a list",
  response_model=List[ReminderItem]
)
async def get_list_id_items(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> List[ReminderItem]:
  """Gets all reminder items for a list."""

  return storage.get_items(list_id)


@router.post(
  path="/reminders/{list_id}/items",
  summary="Add a new item to a reminder list",
  response_model=ReminderItem
)
async def post_reminders_list_id_items(
  list_id: int,
  reminder_item: NewReminderItem,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  """Adds a new item to a reminder list."""

  item_id = storage.add_item(list_id, reminder_item.description)
  return storage.get_item(item_id)


@router.get(
  path="/reminders/items/{item_id}",
  summary="Get a reminder item by ID",
  response_model=ReminderItem
)
async def get_items_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  """Gets a reminder item by ID."""

  return storage.get_item(item_id)


@router.patch(
  path="/reminders/items/{item_id}",
  summary="Update a reminder item's description",
  response_model=ReminderItem
)
async def patch_items_item_id(
  item_id: int,
  reminder_item: NewReminderItem,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  """Updates a reminder item's description."""
  
  storage.update_item_description(item_id, reminder_item.description)
  return storage.get_item(item_id)


@router.patch(
  path="/reminders/items/strike/{item_id}",
  summary="Toggle the completed status of a reminder item",
  response_model=ReminderItem
)
async def patch_items_strike_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  """Toggles the completed status of a reminder item."""
  
  storage.strike_item(item_id)
  return storage.get_item(item_id)


@router.delete(
  path="/reminders/items/{item_id}",
  summary="Deletes a reminder item",
  response_model=Dict
)
async def delete_items_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:
  """Deletes a reminder item by ID."""

  storage.delete_item(item_id)
  return dict()


# --------------------------------------------------------------------------------
# Routes for selected lists
# --------------------------------------------------------------------------------

@router.get(
  path="/reminders/selected",
  summary="Get the selected reminder list",
  response_model=SelectedListId
)
async def get_selected(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> SelectedListId:
  """Gets the selected reminder list."""

  list_id = storage.get_selected_list_id()
  return SelectedListId(list_id=list_id)


@router.post(
  path="/reminders/select/{list_id}",
  summary="Select a reminder list",
  response_model=Dict
)
async def post_select_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:
  """Selects a reminder list."""

  storage.set_selected_list(list_id)
  return {}


@router.post(
  path="/reminders/unselect",
  summary="Unselect any reminder list",
  response_model=Dict
)
async def post_unselect(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:
  """Unselects any reminder list."""

  storage.set_selected_list(None)
  return {}


# --------------------------------------------------------------------------------
# Routes for data management
# --------------------------------------------------------------------------------

@router.delete(
  path="/reminders/delete-lists",
  summary="Delete all the user's reminder lists",
  response_model=Dict
)
async def delete_delete_lists(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:
  """Deletes all the user's reminder lists."""

  storage.delete_lists()
  return {}


@router.post(
  path="/reminders/create-new-lists",
  summary="Create an entirely new set of reminders after deleting old reminders",
  response_model=Dict
)
async def post_create_new_lists(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:
  """Creates an entirely new set of reminders after deleting old reminders."""

  storage.delete_lists()

  # Chores
  chores_id = storage.create_list("Chores")
  storage.set_selected_list(chores_id)
  storage.add_item(chores_id, "Buy groceries")
  storage.add_item(chores_id, "Mow the lawn")
  storage.strike_item(storage.add_item(chores_id, "Walk the dog"))
  storage.strike_item(storage.add_item(chores_id, "Wash the dishes"))
  storage.add_item(chores_id, "Do laundry")

  # Groceries
  groceries_id = storage.create_list("Groceries")
  storage.add_item(groceries_id, "Tomatoes")
  storage.add_item(groceries_id, "Garlic")
  storage.add_item(groceries_id, "Olive oil")
  storage.add_item(groceries_id, "Spaghetti")
  storage.add_item(groceries_id, "Parmesan cheese")
  storage.add_item(groceries_id, "Garlic bread")

  # Projects
  projects_id = storage.create_list("Projects")
  storage.strike_item(storage.add_item(projects_id, "Paint the fence"))
  storage.add_item(projects_id, "Replace the toilet")
  storage.add_item(projects_id, "Install new curtain rods")

  return {}
