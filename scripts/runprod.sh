#!/bin/sh

gunicorn 'app.app:create_app()' --bind 0.0.0.0:8080 --workers 1