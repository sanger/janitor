import ssl

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
