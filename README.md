# reminders-web-app

A web app for reminders built using FastAPI and HTMX


## Running the app

```
uvicorn main:app --reload
```


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