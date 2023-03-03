"""
This module provides routes for status.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import APIRouter
from pydantic import BaseModel


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/api")


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class ReminderItem(BaseModel):
  order: int
  description: str
  completed: bool


class ReminderList(BaseModel):
  id: int
  owner: int
  name: str
  reminders: list[ReminderItem]


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get("/lists", summary="Get the user's reminder lists", response_model=list[ReminderList])
def get_status():
  """
  Gets the list of all reminder lists owned by the user.
  """

  return [
    ReminderList(
      id=1,
      owner=1,
      name="Groceries",
      reminders=[
        ReminderItem(order=1, description="Apple juice", completed=False),
        ReminderItem(order=2, description="Ribs", completed=False),
        ReminderItem(order=3, description="Cheese", completed=True),
      ]
    ),
    ReminderList(
      id=2,
      owner=1,
      name="Chores",
      reminders=[
        ReminderItem(order=1, description="Mow the lawn", completed=False),
        ReminderItem(order=2, description="Feed the dog", completed=True),
        ReminderItem(order=3, description="Do laundry", completed=False),
        ReminderItem(order=4, description="Vacuum", completed=False),
      ]
    ),
  ]


@router.get("/lists/{list_id}", summary="Get a reminder list by ID", response_model=ReminderList)
def get_status(list_id: int):
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
