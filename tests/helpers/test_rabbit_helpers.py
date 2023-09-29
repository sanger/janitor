from datetime import datetime
from unittest.mock import call, mock_open, patch

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from janitor.helpers.rabbit_helpers import batch_messages, rabbit_connection, ssl_rabbit_connection
from janitor.types import RabbitMQDetails


def test_given_list_of_messages_when_creating_batches_then_check_messages_batched_correctly():
    test_messages = [{"message_no:": 1}, {"message_no:": 2}, {"message_no:": 3}, {"message_no:": 4}, {"message_no:": 5}]
    test_batch_size = 2

    expected_messages = [test_messages[0:2], test_messages[2:4], [test_messages[4]]]
    actual_messages = list(batch_messages(test_messages, test_batch_size))

    assert actual_messages == expected_messages


@patch("janitor.helpers.rabbit_helpers.BlockingConnection._create_connection", autospec=True)
def test_given_rabbitmq_details_when_creating_connection_then_check_connection_is_returned(mock_blocking_connection):
    test_rabbitmq_details = RabbitMQDetails(
        USERNAME="test_username", PASSWORD="test_password", HOST="test_host", PORT=5672, VHOST="test_vhost"
    )
    test_rabbit_connection = rabbit_connection(test_rabbitmq_details)

    assert type(test_rabbit_connection) == BlockingConnection
