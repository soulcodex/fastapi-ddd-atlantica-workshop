import databases
from fastapi import FastAPI

MYSQL_POOL_FASTAPI_LS_STATE_KEY = 'mysql_connection_pool'


def fetch_mysql_database_pool(application: FastAPI):
    async def handler() -> databases.Database:
        return getattr(application.state, MYSQL_POOL_FASTAPI_LS_STATE_KEY)

    return handler
