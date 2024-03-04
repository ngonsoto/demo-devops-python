#!/bin/bash

# load environment variables
source .env

# migrate database
python manage.py makemigrations
python manage.py migrate

# run application
python manage.py runserver 0.0.0.0:8000