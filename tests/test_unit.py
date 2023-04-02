"""
This module contains unit tests for the Bulldoggy app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.auth import serialize_token, deserialize_token
from testlib.inputs import User


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_token_serialization(user: User):
  token = serialize_token(user.username)
  assert token
  assert isinstance(token, str)
  assert token != user.username

  username = deserialize_token(token)
  assert username == user.username
