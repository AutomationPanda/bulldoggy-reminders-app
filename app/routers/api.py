"""
This module provides routes for status.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .. import db

from fastapi import APIRouter, Cookie, Response
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/api")


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class ReminderItem(BaseModel):
  description: str
  completed: bool


class ReminderList(BaseModel):
  id: int
  owner: int
  name: str
  reminders: list[ReminderItem]


class NewReminderList(BaseModel):
  name: str


class UpdatedReminderList(BaseModel):
  name: str
  reminders: list[ReminderItem]


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/lists", summary="Get the user's reminder lists", response_model=list[ReminderList])
async def get_lists() -> list[ReminderList]:
  """
  Gets the list of all reminder lists owned by the user.
  """

  return [
    ReminderList(
      id=1,
      owner=1,
      name="Groceries",
      reminders=[
        ReminderItem(description="Apple juice", completed=False),
        ReminderItem(description="Ribs", completed=False),
        ReminderItem(description="Cheese", completed=True),
      ]
    ),
    ReminderList(
      id=2,
      owner=1,
      name="Chores",
      reminders=[
        ReminderItem(description="Mow the lawn", completed=False),
        ReminderItem(description="Feed the dog", completed=True),
        ReminderItem(description="Do laundry", completed=False),
        ReminderItem(description="Vacuum", completed=False),
      ]
    ),
  ]


@router.post("/lists", summary="Create a new reminder list", response_model=ReminderList)
async def post_lists(reminder_list: NewReminderList) -> ReminderList:
  """
  Creates a new reminder list for the user.
  """

  # new_list = reminder_list.dict()
  # new_list["reminders"] = list()
  # new_list["owner"] = 1

  # table = db.table('reminder_lists')
  # list_id = table.insert(new_list)
  
  # # TODO: read this from the database
  # new_list["id"] = list_id
  # return new_list

  return ReminderList(
    id=1,
    owner=1,
    name="Groceries",
    reminders=[
      ReminderItem(order=1, description="Apple juice", completed=False),
      ReminderItem(order=2, description="Ribs", completed=False),
      ReminderItem(order=3, description="Cheese", completed=True),
    ]
  )


@router.get("/lists/{list_id}", summary="Get a reminder list by ID", response_model=ReminderList)
async def get_lists_id(list_id: int) -> ReminderList:
  """
  Gets the reminder list by ID.
  """

  return ReminderList(
    id=1,
    owner=1,
    name="Groceries",
    reminders=[
      ReminderItem(order=1, description="Apple juice", completed=False),
      ReminderItem(order=2, description="Ribs", completed=False),
      ReminderItem(order=3, description="Cheese", completed=True),
    ]
  )


@router.put("/lists/{list_id}", summary="Fully updates a reminder list", response_model=ReminderList)
async def put_lists_id(reminder_list: UpdatedReminderList) -> ReminderList:
  """
  Fully updates a reminder list for the user.
  """
  
  return ReminderList(
    id=1,
    owner=1,
    name="Groceries",
    reminders=[
      ReminderItem(order=1, description="Apple juice", completed=False),
      ReminderItem(order=2, description="Ribs", completed=False),
      ReminderItem(order=3, description="Cheese", completed=True),
    ]
  )


@router.delete("/lists/{list_id}", summary="Deletes a reminder list", response_model=dict)
async def delete_lists_id(list_id: int) -> dict:
  """
  Deletes the reminder list by ID.
  """

  return dict()




class UserAccount(BaseModel):
  username: str
  password: str


@router.post("/login", summary="Logs into the app")
async def post_login(user: UserAccount, response: Response) -> dict():
  response.set_cookie(key="session", value=user.username)
  return {"message": f"Logged in as {user.username}"}


@router.get("/items")
async def read_items(session: str | None = Cookie(default=None)) -> dict:
  return {"session": session}
