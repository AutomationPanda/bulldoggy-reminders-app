"""
This module handles the persistence layer (the "database") for the app
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.exceptions import NotFoundException, ForbiddenException

from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import List


# --------------------------------------------------------------------------------
# RemindersTable Class
# --------------------------------------------------------------------------------

class RemindersTable:
  

  def __init__(self, db_path: str = 'reminder_db.json') -> None:
    self._db_path = db_path
    self._db = TinyDB(db_path)
    self._table = self._db.table('reminders')


  def create_list(self, reminder_list: dict) -> int:
    if reminder_list["reminders"] is None:
      reminder_list["reminders"] = list()

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
    reminder_list = self.get_list(reminders_id, username)
    self._table.update(reminder_list, doc_ids=[reminders_id])
  