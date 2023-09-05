import json
from io import StringIO
from typing import Any, Dict, Sequence, cast

from fastavro import json_writer, parse_schema
from pika import BasicProperties, BlockingConnection


class Publisher:
    """
    Basic publisher class for sending messages to RabbitMQ.
    """

    def __init__(self, connection: BlockingConnection, exchange: str, schema_filepath: str):
        """Load the schema file ready to publish a message to the specified exchange.

        Arguments:
            connection {BlockingConnection}: RabbitMQ connection
            exchange {str}: RabbitMQ exchange to send messages to
            schema_filepath {str}: filepath to schema file
        """
        self._connection = connection
        self._exchange = exchange
        self._schema_filepath = schema_filepath

    @property
    def schema(self):
        """
        Return RabbitMQ connection.
        """
        if self._schema is None:
            with open(self._schema_filepath) as schema_file:
                self._schema = parse_schema(json.load(schema_file))

        return self._schema

    def serialise_message(self, message: Sequence[Dict[str, Any]]) -> bytes:
        """
        Serialise the message using the message schema.

        Arguments:
            message {Sequence[Dict[str, Any]]}: message to be serialised

        Returns:
            {bytes}: Serialised message ready to be published
        """
        string_writer = StringIO()
        json_writer(string_writer, self.schema, message)

        return cast(bytes, string_writer.getvalue())

    def publish_message(
        self, headers: Dict[str, str], message_dicts: Sequence[Dict[str, Any]], routing_key: str = ""
    ) -> None:
        """
        Publish a message to the exchange.

        Arguments:
            headers {Dict[str, str]}: message headers
            message_dicts {Sequence[Dict[str, Any]]}: message to be published
            routing {str}: routing key if sending to specific queues
        """
        channel = self._connection.channel()
        channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            properties=BasicProperties(headers=headers),
            body=self.serialise_message(message_dicts),
        )
