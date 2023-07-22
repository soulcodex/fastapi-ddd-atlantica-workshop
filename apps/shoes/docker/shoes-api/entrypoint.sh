#!/bin/sh

# Run database migrations
pipenv run pyway migrate

# Bootstrap FastAPI with Uvicorn workers
pipenv run uvicorn apps.shoes.main:create_app --factory --reload --host 0.0.0.0