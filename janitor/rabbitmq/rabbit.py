import logging
import math
from typing import Any, Dict, Optional, Sequence, cast

from pika import BlockingConnection

from janitor.helpers.rabbit_helpers import batch_messages, rabbit_connection
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
    def connection(self) -> Optional[BlockingConnection]:
        """
        Return RabbitMQ connection.
        """
        if self._connection is not None:
            return self._connection

        logger.info(f"Attempting to connect to {self._server_details['HOST']}...")
        logger.info(f"VHost: {self._server_details['VHOST']} Port: {self._server_details['PORT']}")

        try:
            self._connection = rabbit_connection(self._server_details)
        except Exception as e:
            logger.error(f"Exception on connecting to RabbitMQ: {e}")
            self._connection = None
            raise

        return self._connection

    def close(self) -> None:
        """
        Close connection to RabbitMQ.
        """
        if self._connection is not None:
            logger.info("Closing connection to RabbitMQ...")
            self._connection.close()
            self._connection = None

    def batch_publish_messages(
        self,
        exchange: str,
        schema_filepath: str,
        headers: Dict[str, str],
        message_dicts: Sequence[Any],
        batch_size: int = 1,
    ) -> Optional[Sequence[Any]]:
        """
        Publish messages in batches to the specified RabbitMQ exchange using a message schema file.

        Arguments:
            exchange {str}: exchange to send message to
            schema_filepath {str}: filepath to message schema file
            headers {Dict[str, str]}: message headers
            message_dicts {Sequence[Any]}: messages to publish
            batch_size {int}: batch size if publishing messages in batches
        """
        if not self.connection:
            logger.error("Not connected to RabbitMQ!")
            return None

        if len(message_dicts) == 0:
            logger.error("No messages to publish to RabbitMQ!")
            return None

        producer = Publisher(connection=self.connection, exchange=exchange, schema_filepath=schema_filepath)
        logger.info(f"Publishing messages to exchange: {exchange}")
        num_messages = math.ceil(len(message_dicts) / batch_size)

        logger.info(f"Publishing messages in batches of size {batch_size}")
        message_dicts = cast(Sequence[Any], batch_messages(message_dicts, batch_size))

        try:
            for message_batch in message_dicts:
                producer.publish_message(headers=headers, message_dicts=message_batch)
        except Exception as e:
            logger.error(f"Exception on publishing to RabbitMQ: {e}")
            logger.error("Failed to publish batch.")
            return cast(Sequence[Any], message_batch)
        else:
            logger.info(f"Published {num_messages} messages!")
            return None
