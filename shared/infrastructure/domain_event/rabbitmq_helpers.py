import aio_pika
from typing import AsyncIterator, Text


async def create_rabbitmq_connection(
        user: Text,
        password: Text,
        host: Text,
        port: Text,
        virtual_host: Text
) -> AsyncIterator[aio_pika.Connection]:
    url = f'amqp://{user}:{password}@{host}:{port}/{virtual_host}'
    client = await aio_pika.connect_robust(url=url)
    yield client
    await client.close()

