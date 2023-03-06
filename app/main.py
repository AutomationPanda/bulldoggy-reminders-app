"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.utils.exceptions import UnauthorizedPageException
from app.routers import api, login, reminders


# --------------------------------------------------------------------------------
# App Creation
# --------------------------------------------------------------------------------

app = FastAPI()
app.include_router(api.router)
app.include_router(login.router)
app.include_router(reminders.router)


# --------------------------------------------------------------------------------
# Static Files
# --------------------------------------------------------------------------------

app.mount( "/static", StaticFiles(directory="static"), name="static")


# --------------------------------------------------------------------------------
# Exception Handlers
# --------------------------------------------------------------------------------

@app.exception_handler(UnauthorizedPageException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedPageException):
  return RedirectResponse('/login?unauthorized=True', status_code=302)


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@app.get("/")
def read_root():
  return {"Hello": "World"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/img/favicon.ico")
