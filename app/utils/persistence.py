"""
This module handles the persistence layer (the "database") for the app
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.exceptions import NotFoundException, ForbiddenException

from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import List, Optional


# --------------------------------------------------------------------------------
# RemindersTable Class
# --------------------------------------------------------------------------------

class RemindersTable:
  

  def __init__(self, db: TinyDB) -> None:
    self._db = db
    self._table = self._db.table('reminders')


  def create_list(self, name: str, username: str, reminders: Optional[List] = None) -> int:
    reminder_list = {
      'name': name,
      'owner': username,
      'reminders': list() if reminders is None else reminders
    }

    list_id = self._table.insert(reminder_list)
    return list_id
  

  def delete_list(self, reminders_id: int, username: str) -> None:
    self.get_list(reminders_id, username)
    self._table.remove(doc_ids=[reminders_id])


  def get_list(self, reminders_id: int, username: str) -> Document:
    reminder_list = self._table.get(doc_id=reminders_id)

    if not reminder_list:
      raise NotFoundException()
    elif reminder_list["owner"] != username:
      raise ForbiddenException()

    reminder_list['id'] = reminders_id
    return reminder_list


  def get_lists(self, username: str) -> List[Document]:
    ListQuery = Query()
    reminder_lists = self._table.search(ListQuery.owner == username)

    for rems in reminder_lists:
      rems['id'] = rems.doc_id

    return reminder_lists
  

  def update_list(self, reminders_id: int, reminder_list: dict, username: str) -> None:
    self.get_list(reminders_id, username)
    self._table.update(reminder_list, doc_ids=[reminders_id])
  

  def update_list_name(self, reminders_id: int, username: str, new_name: str) -> None:
    reminder_list = self.get_list(reminders_id, username)
    reminder_list['name'] = new_name
    self._table.update(reminder_list, doc_ids=[reminders_id])
  