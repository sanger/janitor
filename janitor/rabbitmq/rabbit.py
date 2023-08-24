import logging
from typing import Any, Dict, Optional, Sequence

from pika import BlockingConnection

from janitor.helpers.rabbit_helpers import rabbit_connection
from janitor.rabbitmq.publisher import Publisher
from janitor.types import RabbitMQDetails

logger = logging.getLogger(__name__)


class Rabbit:
    """
    Basic class for connecting to RabbitMQ using specified details. This class can be used for publishing messages.
    """

    def __init__(self, server_details: RabbitMQDetails):
        """
        Use server details and login credentials to open RabbitMQ connection when needed.
        """
        self._server_details = server_details
        self._connection: Optional[BlockingConnection] = None

    @property
    def connection(self) -> BlockingConnection:
        """
        Return RabbitMQ connection.
        """
        if self._connection is None:
            return rabbit_connection(self._server_details)

        return self._connection

    def publish_message(
        self, exchange: str, schema_filepath: str, headers: Dict[str, str], message_dicts: Sequence[Any]
    ) -> None:
        """
        Publish a message to the specified RabbitMQ exchange using a message schema file.

        Arguments:
            exchange {str}: exchange to send message to
            schema_filepath {str}: filepath to message schema file
            headers {Dict[str, str]}: message headers
            message_dicts {Sequence[Any]}: message to publish
        """
        producer = Publisher(connection=self.connection, exchange=exchange, schema_filepath=schema_filepath)
        logger.info(f"Publishing message to exchange: {exchange}")
        logger.info(f"Message: {message_dicts}")
        producer.publish_message(headers=headers, message_dicts=message_dicts)
        logger.info("Message published!")
