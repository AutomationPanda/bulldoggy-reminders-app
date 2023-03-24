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
from typing import List, Optional


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


class SelectedList(BaseModel):
  id: int
  owner: str
  name: str
  items: List[ReminderItem]


# --------------------------------------------------------------------------------
# ReminderStorage Class
# --------------------------------------------------------------------------------

class ReminderStorage:
  

  def __init__(self, owner: str, db_path: str = 'reminder_db.json') -> None:
    self.owner = owner
    self._db_path = db_path
    self._db = TinyDB(db_path)
    self._lists_table = self._db.table('reminder_lists')
    self._items_table = self._db.table('reminder_items')
    self._selected_table = self._db.table('selected_lists')


  # Private Methods

  def _get_raw_list(self, list_id: int) -> Document:
    reminder_list = self._lists_table.get(doc_id=list_id)

    if not reminder_list:
      raise NotFoundException()
    elif reminder_list["owner"] != self.owner:
      raise ForbiddenException()
    
    return reminder_list
  

  def _get_raw_item(self, item_id: int) -> Document:
    item = self._items_table.get(doc_id=item_id)
    if not item:
      raise NotFoundException()
    
    self._verify_list_exists(item['list_id'])
    return item


  def _verify_list_exists(self, list_id: int) -> None:
    # Just get the list and make sure no exceptions happen
    self._get_raw_list(list_id)
  

  def _verify_item_exists(self, item_id: int) -> None:
    # Just get the item and make sure no exceptions happen
    self._get_raw_item(item_id)


  # Reminder Lists

  def create_list(self, name: str) -> int:
    reminder_list = {'name': name, 'owner': self.owner}
    list_id = self._lists_table.insert(reminder_list)
    return list_id
  

  def delete_list(self, list_id: int) -> None:
    self._verify_list_exists(list_id)
    self._lists_table.remove(doc_ids=[list_id])
    self._items_table.remove(Query().list_id == list_id)


  def delete_lists(self) -> None:
    for rem_list in self.get_lists():
      self.delete_list(rem_list.id)


  def get_list(self, list_id: int) -> ReminderList:
    reminder_list = self._get_raw_list(list_id)
    reminder_list['id'] = list_id
    model = ReminderList(**reminder_list)
    return model


  def get_lists(self) -> List[ReminderList]:
    reminder_lists = self._lists_table.search(Query().owner == self.owner)
    models = [ReminderList(id=rems.doc_id, **rems) for rems in reminder_lists]
    return models
  

  def update_list_name(self, list_id: int, new_name: str) -> None:
    reminder_list = self._get_raw_list(list_id)
    reminder_list['name'] = new_name
    self._lists_table.update(reminder_list, doc_ids=[list_id])
  

  # Reminder Items

  def add_item(self, list_id: int, description: str) -> int:
    reminder_item = {
      'list_id': list_id,
      'description': description,
      'completed': False,
    }

    self._verify_list_exists(list_id)
    item_id = self._items_table.insert(reminder_item)
    return item_id
  

  def delete_item(self, item_id: int) -> None:
    self._verify_item_exists(item_id)
    self._items_table.remove(doc_ids=[item_id])


  def get_item(self, item_id: int) -> ReminderItem:
    item = self._get_raw_item(item_id)
    item['id'] = item_id
    model = ReminderItem(**item)
    return model


  def get_items(self, list_id: int) -> List[ReminderItem]:
    self._verify_list_exists(list_id)
    items = self._items_table.search(Query().list_id == list_id)
    models = [ReminderItem(id=item.doc_id, ** item) for item in items]
    return models
  

  def strike_item(self, item_id: int) -> None:
    item = self._get_raw_item(item_id)
    item['completed'] = not item['completed']
    self._items_table.update(item, doc_ids=[item_id])
  

  def update_item_description(self, item_id: int, new_description: str) -> None:
    item = self._get_raw_item(item_id)
    item['description'] = new_description
    self._items_table.update(item, doc_ids=[item_id])


  # Selected Lists

  def get_selected_list_id(self) -> Optional[int]:
    selected_list = self._selected_table.search(Query().owner == self.owner)
    if not selected_list:
      return None
    
    list_id = selected_list[0]['list_id']
    return list_id


  def get_selected_list(self) -> Optional[SelectedList]:
    list_id = self.get_selected_list_id()
    if list_id is None:
      return None

    try:
      reminder_list = self.get_list(list_id)
      reminder_items = self.get_items(list_id)
    except:
      self._selected_table.update({'list_id': None}, Query().owner == self.owner)
      return None

    return SelectedList(
      id=reminder_list.id,
      owner=reminder_list.owner,
      name=reminder_list.name,
      items=reminder_items)


  def set_selected_list(self, list_id: Optional[int]) -> None:
    selected_list = self._selected_table.search(Query().owner == self.owner)

    if selected_list:
      self._selected_table.update({'list_id': list_id}, Query().owner == self.owner)
    else:
      self._selected_table.insert({'owner': self.owner, 'list_id': list_id})


  def reset_selected_after_delete(self, deleted_id: int) -> None:
    selected_list = self._selected_table.search(Query().owner == self.owner)

    if selected_list and selected_list[0]['list_id'] == deleted_id:
      reminder_lists = self._lists_table.all()
      list_id = reminder_lists[0].doc_id if reminder_lists else None
      self.set_selected_list(list_id)
