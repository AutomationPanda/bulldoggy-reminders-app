# reminders-web-app

A web app for reminders built using FastAPI and HTMX.
It uses HTMX 1.8.6.


## Running the app

```
uvicorn app.main:app --reload
```


## TODO

* HTMX interactions
  * loading the page
  * hovering over a row shows the icons
  * hovering away from a row removes the icons
  * clicking a reminders list row selects it
  * clicking the edit button enables editing a row
  * clicking the delete button removes a row
  * clicking check while editing updates a row
  * clicking x with editing ignores changes to a row
  * clicking the "new" row enables editing for a new item
  * clicking a reminder item strikes it out
  * clickign a stricken reminder item unstrikes it

* UI tests
* API tests (?)
