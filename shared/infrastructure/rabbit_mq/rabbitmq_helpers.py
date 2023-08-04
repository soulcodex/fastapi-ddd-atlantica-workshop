import asyncio
import aio_pika
from yarl import URL
from typing import AsyncIterator, Text


def create_rabbitmq_connection(
        user: Text,
        password: Text,
        host: Text,
        port: Text,
        virtual_host: Text
) -> aio_pika.Connection:
    url = f'amqp://{user}:{password}@{host}:{port}/{virtual_host}'
    return aio_pika.RobustConnection(url=URL(url), loop=asyncio.get_event_loop())
