"""
This module builds shared parts for other modules.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json

from app.utils.persistence import RemindersTable
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB


# --------------------------------------------------------------------------------
# Read Configuration
# --------------------------------------------------------------------------------

with open('config.json') as config_json:
  config = json.load(config_json)
  users = config['users']


# --------------------------------------------------------------------------------
# Establish the Secret Key
# --------------------------------------------------------------------------------

secret_key = config['secret_key']


# --------------------------------------------------------------------------------
# Connect the Database
# --------------------------------------------------------------------------------

db = TinyDB('reminder_db.json')
reminders_table = RemindersTable(db)


# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")
