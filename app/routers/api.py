"""
This module provides routes for the API.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import db
from app.utils.auth import AuthCookie, get_auth_cookie
from app.utils.exceptions import NotFoundException, ForbiddenException

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tinydb import Query


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/api")


# --------------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------------

reminders_table = db.table('reminders')


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class ReminderItem(BaseModel):
  description: str
  completed: bool


class ReminderList(BaseModel):
  id: int
  owner: str
  name: str
  reminders: list[ReminderItem]


class NewReminderList(BaseModel):
  name: str
  reminders: list[ReminderItem] | None


class UpdatedReminderList(BaseModel):
  name: str
  reminders: list[ReminderItem]


# --------------------------------------------------------------------------------
# Query Functions
# --------------------------------------------------------------------------------

def query_reminders_by_id(reminders_id: int, username: str) -> dict:
  reminder_list = reminders_table.get(doc_id=reminders_id)

  if not reminder_list:
    raise NotFoundException()
  elif reminder_list["owner"] != username:
    raise ForbiddenException()

  reminder_list['id'] = reminders_id
  return reminder_list


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/reminders", summary="Get the user's reminder lists", response_model=list[ReminderList])
async def get_reminders(
  cookie: AuthCookie = Depends(get_auth_cookie)
  ) -> list[ReminderList]:
  """
  Gets the list of all reminder lists owned by the user.
  """

  ListQuery = Query()
  reminder_lists = reminders_table.search(ListQuery.owner == cookie.username)

  for rems in reminder_lists:
    rems['id'] = rems.doc_id

  return reminder_lists


@router.post("/reminders", summary="Create a new reminder list", response_model=ReminderList)
async def post_reminders(
  reminder_list: NewReminderList,
  cookie: AuthCookie = Depends(get_auth_cookie)
  ) -> ReminderList:
  """
  Creates a new reminder list for the user.
  """

  new_list = reminder_list.dict()
  new_list["owner"] = cookie.username

  if new_list["reminders"] is None:
    new_list["reminders"] = list()

  list_id = reminders_table.insert(new_list)
  
  return query_reminders_by_id(list_id, cookie.username)


@router.get("/reminders/{reminders_id}", summary="Get a reminder list by ID", response_model=ReminderList)
async def get_reminders_id(
  reminders_id: int,
  cookie: AuthCookie = Depends(get_auth_cookie)
  ) -> ReminderList:
  """
  Gets the reminder list by ID.
  """

  return query_reminders_by_id(reminders_id, cookie.username)


@router.put("/reminders/{reminders_id}", summary="Fully updates a reminder list", response_model=ReminderList)
async def put_reminders_id(
  reminders_id: int,
  reminder_list: UpdatedReminderList,
  cookie: AuthCookie = Depends(get_auth_cookie)
  ) -> ReminderList:
  """
  Fully updates a reminder list for the user.
  """
  
  data = reminder_list.dict()
  query_reminders_by_id(reminders_id, cookie.username)
  reminders_table.update(data, doc_ids=[reminders_id])

  updated_reminders = reminders_table.get(doc_id=reminders_id)
  updated_reminders['id'] = reminders_id
  return updated_reminders


@router.delete("/reminders/{reminders_id}", summary="Deletes a reminder list", response_model=dict)
async def delete_reminders_id(
  reminders_id: int,
  cookie: AuthCookie = Depends(get_auth_cookie)
  ) -> dict:
  """
  Deletes the reminder list by ID.
  """

  query_reminders_by_id(reminders_id, cookie.username)
  reminders_table.remove(doc_ids=[reminders_id])
  return dict()
