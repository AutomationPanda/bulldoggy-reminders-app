# reminders-web-app

A web app for reminders built using FastAPI and HTMX


## Running the app

```
uvicorn main:app --reload
```


## Action plan

* Set up configurable users (like from the DRS)
* Implement cookie-based authentication for those users
* Add authentication to API requests for lists
* Add database implementation to API requests for lists


## Data models

* user
  * username
  * password
* list
  * owner
  * name
  * reminders
    * order
    * description
    * completed