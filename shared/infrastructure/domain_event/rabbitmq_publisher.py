from typing import Text

import aio_pika
import aiormq

from shared.domain.types.domain_event import DomainEventPublisher, DomainEventSerializer, DomainEvent


class RabbitMqEventPublisher(DomainEventPublisher):

    def __init__(self, exchange: Text, client: aio_pika.Connection, serializer: DomainEventSerializer):
        self.client = client
        self._exchange = exchange
        self.serializer = serializer

    async def publish(self, event: DomainEvent) -> None:
        try:
            async with self.client.channel() as channel:
                exchange = await channel.get_exchange(name=self._exchange, ensure=False)
                await exchange.publish(message=await self._message(event), routing_key=event.event_name())
        except aiormq.AMQPException or aiormq.AMQPError:
            pass  # Fail-over publisher like mongodb, mysql, etc ...

    async def _message(self, event: DomainEvent) -> aio_pika.Message:
        body = await self.serializer.serialize(event=event)
        return aio_pika.Message(
            body=body.encode(),
            message_id=event.id.value,
            headers={
                'message_id': event.id.value,
                'content_type': 'application/json',
                'content_encoding': 'utf-8'
            }
        )
