import aio_pika
from fastapi import FastAPI

RABBITMQ_POOL_FASTAPI_LS_STATE_KEY = 'rabbitmq_connection_pool'


def fetch_rabbit_mq_pool(application: FastAPI):
    async def handler() -> aio_pika.Connection:
        return getattr(application.state, RABBITMQ_POOL_FASTAPI_LS_STATE_KEY)

    return handler
