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


  # Reminder Lists

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
  

  # Reminder Items

  def add_list_item(self, reminders_id: int, username: str, new_item: str) -> None:
    reminder_item = {
      'description': new_item,
      'completed': False,
    }

    reminder_list = self.get_list(reminders_id, username)
    reminder_list['reminders'].append(reminder_item)
    self._reminders_table.update(reminder_list, doc_ids=[reminders_id])


  # Selected

  def get_selected_reminders(self, username: str) -> Optional[Document]:
    selected_list = self._selected_table.search(Query().username == username)
    if not selected_list:
      return None
    
    reminders_id = selected_list[0]['reminders_id']
    if reminders_id is None:
      return None

    try:
      reminders_list = self.get_list(reminders_id, username)
    except:
      self._selected_table.update({'reminders_id': None}, Query().username == username)
      return None

    return reminders_list


  def set_selected_reminders(self, reminders_id: Optional[int], username: str) -> None:
    selected_list = self._selected_table.search(Query().username == username)

    if selected_list:
      self._selected_table.update({'reminders_id': reminders_id}, Query().username == username)
    else:
      self._selected_table.insert({'username': username, 'reminders_id': reminders_id})


  def reset_selected_after_delete(self, deleted_id: int, username: str) -> None:
    selected_list = self._selected_table.search(Query().username == username)

    if selected_list and selected_list[0]['reminders_id'] == deleted_id:
      reminder_lists = self._reminders_table.all()
      reminders_id = reminder_lists[0].doc_id if reminder_lists else None
      self.set_selected_reminders(reminders_id, username)
