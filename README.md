![Bulldoggy Logo](static/img/logos/bulldoggy-100px.png)

# Bulldoggy: The Reminders App

*Bulldoggy* is a small demo web app for tracking reminders.
It uses:

* [Python](https://www.python.org/) as the main programming language
* [FastAPI](https://fastapi.tiangolo.com/) for the backend
* [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) for the database
* [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/) with HTML and CSS for the frontend
* [HTMX](https://htmx.org/) 1.8.6 for handling dynamic interactions (instead of raw JavaScript)


## Running the app

To install dependencies and run the app:

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then, open your browser to `http://127.0.0.1:8000` to load the app.


## Logging into the app

The [`config.json`](config.json) file declares the users for the app.
You may use any configured user credentials, or change them to your liking.
The "default" username is `pythonista` with the password `I<3testing`.


## Setting the database path

The app uses TinyDB, which stores the database as a JSON file.
The default database filepath is `reminder_db.json`.
You may change this path in [`config.json`](config.json).
If you change the filepath, the app will automatically create a new, empty database.


## TODO

* Write a better README
* Fix the API
* UI tests
* API tests (?)
