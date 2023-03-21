"""
This module handles the persistence layer (the "database") for the app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.exceptions import NotFoundException, ForbiddenException

from pydantic import BaseModel
from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import Optional


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class ReminderItem(BaseModel):
  id: int
  list_id: int
  description: str
  completed: bool


class ReminderList(BaseModel):
  id: int
  owner: str
  name: str


# --------------------------------------------------------------------------------
# ReminderStorage Class
# --------------------------------------------------------------------------------

class ReminderStorage:
  

  def __init__(self, owner: str, db_path: str = 'reminder_db.json') -> None:
    self.owner = owner
    self._db_path = db_path
    self._db = TinyDB(db_path)
    self._reminder_lists_table = self._db.table('reminder_lists')
    self._reminder_items_table = self._db.table('reminder_items')
    self._selected_table = self._db.table('selected')


  # Private Methods

  def _get_raw_list(self, list_id: int) -> Document:
    reminder_list = self._reminder_lists_table.get(doc_id=list_id)

    if not reminder_list:
      raise NotFoundException()
    elif reminder_list["owner"] != self.owner:
      raise ForbiddenException()
    
    return reminder_list


  # Reminder Lists

  def create_list(self, name: str) -> int:
    reminder_list = {'name': name, 'owner': self.owner}
    list_id = self._reminder_lists_table.insert(reminder_list)
    return list_id
  

  def delete_list(self, list_id: int) -> None:
    self.get_list(list_id)
    self._reminder_lists_table.remove(doc_ids=[list_id])


  def get_list(self, list_id: int) -> ReminderList:
    reminder_list = self._get_raw_list(list_id)
    reminder_list['id'] = list_id
    model = ReminderList(**reminder_list)
    return model


  def get_lists(self) -> list[ReminderList]:
    reminder_lists = self._reminder_lists_table.search(Query().owner == self.owner)
    models = [ReminderList(id=rems.doc_id, **rems) for rems in reminder_lists]
    return models
  

  def update_list_name(self, list_id: int, new_name: str) -> None:
    reminder_list = self._get_raw_list(list_id)
    reminder_list['name'] = new_name
    self._reminder_lists_table.update(reminder_list, doc_ids=[list_id])
  

  # Reminder Items

  # def add_item(self, list_id: int, owner: str, new_item: str) -> None:
  #   reminder_item = {
  #     'description': new_item,
  #     'completed': False,
  #   }

  #   reminder_list = self.get_list(list_id, owner)
  #   reminder_list['reminders'].append(reminder_item)
  #   self._reminder_lists_table.update(reminder_list, doc_ids=[list_id])


  # Selected

  def get_selected_list(self) -> Optional[ReminderList]:
    selected_list = self._selected_table.search(Query().owner == self.owner)
    if not selected_list:
      return None
    
    list_id = selected_list[0]['list_id']
    if list_id is None:
      return None

    try:
      reminders_list = self.get_list(list_id)
    except:
      self._selected_table.update({'list_id': None}, Query().owner == self.owner)
      return None

    return reminders_list


  def set_selected_list(self, list_id: Optional[int]) -> None:
    selected_list = self._selected_table.search(Query().owner == self.owner)

    if selected_list:
      self._selected_table.update({'list_id': list_id}, Query().owner == self.owner)
    else:
      self._selected_table.insert({'owner': self.owner, 'list_id': list_id})


  def reset_selected_after_delete(self, deleted_id: int) -> None:
    selected_list = self._selected_table.search(Query().owner == self.owner)

    if selected_list and selected_list[0]['list_id'] == deleted_id:
      reminder_lists = self._reminder_lists_table.all()
      list_id = reminder_lists[0].doc_id if reminder_lists else None
      self.set_selected_list(list_id)
