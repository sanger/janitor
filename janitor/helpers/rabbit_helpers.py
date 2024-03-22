import ssl
from typing import Any, Generator, Mapping, Sequence

from pika import BlockingConnection, ConnectionParameters, PlainCredentials, SSLOptions

from janitor.types import RabbitMQDetails


def rabbit_connection(rabbitmq_details: RabbitMQDetails) -> BlockingConnection:
    """
    Create a connection to RabbitMQ.

    Arguments:
        rabbitmq_details {RabbitMQDetails}: server details for RabbitMQ

    Returns:
        {BlockingConnection}: RabbitMQ connection
    """
    credentials = PlainCredentials(rabbitmq_details["USERNAME"], rabbitmq_details["PASSWORD"])
    connection_params = ConnectionParameters(
        host=rabbitmq_details["HOST"],
        port=rabbitmq_details["PORT"],
        virtual_host=rabbitmq_details["VHOST"],
        credentials=credentials,
    )

    return BlockingConnection(connection_params)


def ssl_rabbit_connection(rabbitmq_details: RabbitMQDetails) -> BlockingConnection:
    """
    Create a connection to RabbitMQ using SSL.

    Arguments:
        rabbitmq_details {RabbitMQDetails}: server details for RabbitMQ

    Returns:
        {BlockingConnection}: RabbitMQ connection
    """
    credentials = PlainCredentials(rabbitmq_details["USERNAME"], rabbitmq_details["PASSWORD"])
    ssl_context = ssl.create_default_context()
    connection_params = ConnectionParameters(
        host=rabbitmq_details["HOST"],
        port=rabbitmq_details["PORT"],
        virtual_host=rabbitmq_details["VHOST"],
        credentials=credentials,
        ssl_options=SSLOptions(ssl_context),
    )

    return BlockingConnection(connection_params)


def batch_messages(message_dicts: Sequence[Mapping[str, Any]], batch_size: int) -> Generator:
    """
    Split up messages into batches of specified size.

    Arguments:
        message_dicts {Sequence[Mapping[str, Any]]}: messages to split into batches
        batch_size {int}: Size of each batch of messages
    """
    for message_index in range(0, len(message_dicts), batch_size):
        yield message_dicts[message_index : message_index + batch_size]
