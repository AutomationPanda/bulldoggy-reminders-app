"""
This module provides fixtures for testing.

WARNING:
Why don't we just use command line arguments for base URL and passwords?
Because it's annoying to type them out every time we want to run tests!

TODO: storage state for UI and API
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest

from playwright.sync_api import Playwright
from testlib.inputs import User


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(inputs, index):
  assert 'users' in inputs, "inputs are missing 'users' key"
  users = inputs['users']

  assert len(users) > index, f"index {index} is out of range for input 'users'"
  assert 'username' in users[index], f"input 'users[{index}]' is missing 'username'"
  assert 'password' in users[index], f"input 'users[{index}]' is missing 'password'"
  user = User(users[index]['username'], users[index]['password'])

  return user


# --------------------------------------------------------------------------------
# Input Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_inputs():
  with open('inputs.json') as inputs_json:
    data = json.load(inputs_json)
  return data


@pytest.fixture(scope='session')
def base_url(test_inputs):
  assert 'base_url' in test_inputs, "inputs are missing 'base_url' key"
  return test_inputs['base_url']


@pytest.fixture(scope='session')
def user(test_inputs):
  return _build_user(test_inputs, 0)


@pytest.fixture(scope='session')
def alt_user(test_inputs):
  return _build_user(test_inputs, 1)


# --------------------------------------------------------------------------------
# Playwright Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def bulldoggy_api(playwright: Playwright, base_url: str):
  return playwright.request.new_context(base_url=base_url)
