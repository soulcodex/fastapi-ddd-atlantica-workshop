#!/bin/sh

# Run database migrations
pipenv run pyway migrate

# Bootstrap FastAPI with Uvicorn workers
pipenv run uvicorn apps.shoes.main:app --reload --host 0.0.0.0