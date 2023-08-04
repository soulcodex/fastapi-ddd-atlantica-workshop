import aio_pika
import databases
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.datastructures import State
from apps.shoes.dependency_injection import common

from shared.infrastructure.mysql.fastapi_helpers import MYSQL_POOL_FASTAPI_LS_STATE_KEY, \
    fetch_mysql_database_pool
from shared.infrastructure.rabbit_mq.fastapi_helpers import RABBITMQ_POOL_FASTAPI_LS_STATE_KEY, \
    fetch_rabbit_mq_pool


async def startup_lifespan_handler(application: FastAPI):
    environment = await common.configure_environment_handler()

    # Database (MySQL)
    database = await common.configure_database_connection_pool(environment)
    await database.connect()
    setattr(application.state, MYSQL_POOL_FASTAPI_LS_STATE_KEY, database)
    mysql_pool_getter = fetch_mysql_database_pool(application)
    application.dependency_overrides[common.configure_database_connection_pool] = mysql_pool_getter

    # Message message_broker_connection (RabbitMQ)
    message_broker_connection = await common.configure_rabbitmq_connection(environment)
    await message_broker_connection.connect()
    setattr(application.state, RABBITMQ_POOL_FASTAPI_LS_STATE_KEY, message_broker_connection)
    rabbitmq_pool_getter = fetch_rabbit_mq_pool(application)
    application.dependency_overrides[common.configure_rabbitmq_connection] = rabbitmq_pool_getter


async def shutdown_lifespan_handler(application: FastAPI):
    database = getattr(application.state, MYSQL_POOL_FASTAPI_LS_STATE_KEY)
    message_broker_connection = getattr(application.state, RABBITMQ_POOL_FASTAPI_LS_STATE_KEY)
    await database.disconnect()
    await message_broker_connection.close()
    setattr(application, 'state', State())


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    await startup_lifespan_handler(app)
    yield
    await shutdown_lifespan_handler(app)
