![Bulldoggy Logo](static/img/logos/bulldoggy-100px.png)

# Bulldoggy: The Reminders App

*Bulldoggy* is a small demo web app for tracking reminders.
It uses:

* [Python](https://www.python.org/) as the main programming language
* [FastAPI](https://fastapi.tiangolo.com/) for the backend
* [HTMX](https://htmx.org/) 1.8.6 for handling dynamic interactions (instead of raw JavaScript)
* [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/) with HTML and CSS for the frontend
* [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) for the database
* [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/) for testing


## Installing dependencies

You will need a recent version of Python to run this app.
To install project dependencies:

```
pip install -r requirements.txt
```

It is recommended to install dependencies into a [virtual environment](https://docs.python.org/3/library/venv.html).


## Running the app

To run the app:

```
uvicorn app.main:app --reload
```

Then, open your browser to [`http://127.0.0.1:8000`](http://127.0.0.1:8000) to load the app.


## Logging into the app

The [`config.json`](config.json) file declares the users for the app.
You may use any configured user credentials, or change them to your liking.
The "default" username is `pythonista` with the password `I<3testing`.


## Setting the database path

The app uses TinyDB, which stores the database as a JSON file.
The default database filepath is `reminder_db.json`.
You may change this path in [`config.json`](config.json).
If you change the filepath, the app will automatically create a new, empty database.


## Using the app

Bulldoggy is a reminders app.
After you log in, you can create reminder lists.

![Bulldoggy login](static/img/readme/bulldoggy-login.png)

Each reminder list appears on the left,
and the items in the list appear on the right.
You may add, delete, or edit lists and items.
You may also strike out completed items.

![Bulldoggy reminders](static/img/readme/bulldoggy-reminders.png)


## Reading the docs

To read the API docs, open the following pages:

* [`/docs`](http://127.0.0.1:8000/docs) for classic OpenAPI docs
* [`/redoc`](http://127.0.0.1:8000/redoc) for more modern ReDoc docs


## Why did I build this app in Python?

Personally, I love Python, and I wanted to demonstrate how to **build a full-stack modern web app *entirely* with Python**.

JavaScript essentially has a near-monopoly on front-end web development.
Browsers require JavaScript code to perform dynamic web page interactions.
However, [HTMX](https://htmx.org/) offers a novel way to sidestep this limitation:
it provides special HTML attributes to denote dynamic interactions for elements.
Under the hood, HTMX uses AJAX to issue HTTP requests and swap hypertext contents for elements targetted with its special attributes.
JavaScript is still there – you just don't need to touch it!

This enables web frameworks in languages like Python, Go, Java, and others to offer dynamic web page content
directly in HTML *without* requiring developers to explicitly code any JavaScript.
HTMX empowers you, as a developer, to build beautiful web apps while remaining in the tech stack of your choice!


## TODO list

* Automate API tests
* Automate UI tests
