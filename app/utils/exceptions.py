"""
This module provides exceptions for the app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import HTTPException, status


# --------------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------------

class UnauthorizedException(HTTPException):
  def __init__(self):
    super().__init__(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


class UnauthorizedPageException(HTTPException):
  def __init__(self):
    super().__init__(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


class ForbiddenException(HTTPException):
  def __init__(self):
    super().__init__(status.HTTP_403_FORBIDDEN, "Forbidden")


class NotFoundException(HTTPException):
  def __init__(self):
    super().__init__(status.HTTP_404_NOT_FOUND, "Not Found")
