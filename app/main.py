"""
This module is the main module for the FastAPI app.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app.utils.exceptions import UnauthorizedPageException
from app.routers import api, login, reminders, root

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException


# --------------------------------------------------------------------------------
# App Creation
# --------------------------------------------------------------------------------

app = FastAPI()
app.include_router(root.router)
app.include_router(api.router)
app.include_router(login.router)
app.include_router(reminders.router)


# --------------------------------------------------------------------------------
# Static Files
# --------------------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")


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
# OpenAPI Customization
# --------------------------------------------------------------------------------

def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema
  
  description = \
    """Bulldoggy is a web app for tracking reminders.
    It is a full-stack Python app built using FastAPI and HTMX.
    It is meant to be an "example" or "demo" app used for instructional purposes.
    """

  openapi_schema = get_openapi(
    title="Bulldoggy: The Reminders App",
    version="1.0.0",
    description=description,
    routes=app.routes,
    tags=[
      {
        "name": "API",
        "description": "Backend API routes for managing reminder lists and items.",
      },
      {
        "name": "Pages",
        "description": "The main Bulldoggy web pages.",
      },
      {
        "name": "Authentication",
        "description": "Routes for logging into and out of the app.",
      },
      {
        "name": "HTMX Partials",
        "description": "Routes that serve partial web page contents for HTMX-based requests.",
      },
    ]
  )

  openapi_schema["info"]["x-logo"] = {
    "url": "static/img/logos/bulldoggy-500px.png"
  }

  app.openapi_schema = openapi_schema
  return app.openapi_schema


app.openapi = custom_openapi
