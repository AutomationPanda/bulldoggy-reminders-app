"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import AuthCookie, get_auth_cookie
from app.utils.exceptions import UnauthorizedPageException
from app.routers import api, login, reminders

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from typing import Optional


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


@app.exception_handler(404)
async def page_not_found_exception_handler(request: Request, exc: HTTPException):
  if request.url.path.startswith('/api/'):
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
  else:
    return RedirectResponse('/not-found')


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@app.get(
  path="/",
  summary="Redirects to the login or reminders pages",
  tags=["Pages"]
)
async def read_root(cookie: Optional[AuthCookie] = Depends(get_auth_cookie)):
  path = '/reminders' if cookie else '/login'
  return RedirectResponse(path, status_code=302)


@app.get(
  path='/favicon.ico',
  include_in_schema=False
)
async def get_favicon():
  return FileResponse("static/img/favicon.ico")


@app.get(
  path='/not-found',
  summary="Gets the \"Not Found\" page",
  tags=["Pages"]
)
async def get_not_found(request: Request):
  return templates.TemplateResponse("pages/not-found.html", {'request': request})
