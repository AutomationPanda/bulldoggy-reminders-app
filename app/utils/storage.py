"""
This module handles the persistence layer (the "database") for the app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.exceptions import NotFoundException, ForbiddenException

from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import List, Optional


# --------------------------------------------------------------------------------
# ReminderStorage Class
# --------------------------------------------------------------------------------

class ReminderStorage:
  

  def __init__(self, db_path: str = 'reminder_db.json') -> None:
    self._db_path = db_path
    self._db = TinyDB(db_path)
    self._reminders_table = self._db.table('reminders')
    self._selected_table = self._db.table('selected')


  # Reminders

  def create_list(self, name: str, username: str, reminders: Optional[List] = None) -> int:
    reminder_list = {
      'name': name,
      'owner': username,
      'reminders': list() if reminders is None else reminders
    }

    list_id = self._reminders_table.insert(reminder_list)
    return list_id
  

  def delete_list(self, reminders_id: int, username: str) -> None:
    self.get_list(reminders_id, username)
    self._reminders_table.remove(doc_ids=[reminders_id])


  def get_list(self, reminders_id: int, username: str) -> Document:
    reminder_list = self._reminders_table.get(doc_id=reminders_id)

    if not reminder_list:
      raise NotFoundException()
    elif reminder_list["owner"] != username:
      raise ForbiddenException()

    reminder_list['id'] = reminders_id
    return reminder_list


  def get_lists(self, username: str) -> List[Document]:
    list_query = Query()
    reminder_lists = self._reminders_table.search(list_query.owner == username)

    for rems in reminder_lists:
      rems['id'] = rems.doc_id

    return reminder_lists
  

  def update_list(self, reminders_id: int, reminder_list: dict, username: str) -> None:
    self.get_list(reminders_id, username)
    self._reminders_table.update(reminder_list, doc_ids=[reminders_id])
  

  def update_list_name(self, reminders_id: int, username: str, new_name: str) -> None:
    reminder_list = self.get_list(reminders_id, username)
    reminder_list['name'] = new_name
    self._reminders_table.update(reminder_list, doc_ids=[reminders_id])
  

  # Selected

  def get_selected_reminders(self, username: str) -> Optional[int]:
    selected_list = self._selected_table.search(Query().username == username)
    return selected_list[0]['reminders_id'] if selected_list else None


  def set_selected_reminders(self, reminders_id: Optional[int], username: str) -> None:
    selected_list = self._selected_table.search(Query().username == username)

    if selected_list:
      self._selected_table.update({'reminders_id': reminders_id}, Query().username == username)
    else:
      self._selected_table.insert({'username': username, 'reminders_id': reminders_id})
