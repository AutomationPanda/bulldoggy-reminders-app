FROM python:3

WORKDIR /bulldoggy-reminders-app

# Install the requirements
COPY ./requirements.txt /bulldoggy-reminders-app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bulldoggy-reminders-app/requirements.txt

# Copy the app folders and files
COPY ./app /bulldoggy-reminders-app/app
COPY ./static /bulldoggy-reminders-app/static
COPY ./templates /bulldoggy-reminders-app/templates
COPY config.json /bulldoggy-reminders-app/config.json

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]