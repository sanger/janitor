from unittest.mock import PropertyMock, call, patch

from janitor.rabbitmq.rabbit import Rabbit
from janitor.types import RabbitMQDetails

test_config = RabbitMQDetails(
    USERNAME="rabbitmq_test_username",
    PASSWORD="rabbitmq_test_password",
    HOST="rabbitmq_test_host",
    PORT=5672,
    VHOST="rabbitmq_test_vhost",
)

TEST_EXCHANGE = "test_exchange"
TEST_SCHEMA_FILEPATH = "test_schema_filepath"
TEST_BATCH_SIZE = 2
TEST_MESSAGES = [
    {"message_no": 1},
    {"message_no": 2},
    {"message_no": 3},
    {"message_no": 4},
]


def test_given_test_config_when_creating_rabbit_connection_then_check_connection_has_correct_parameters():
    test_rabbit = Rabbit(test_config)

    assert test_rabbit._server_details["HOST"] == test_config["HOST"]
    assert test_rabbit._server_details["VHOST"] == test_config["VHOST"]
    assert test_rabbit._server_details["PORT"] == test_config["PORT"]
    assert test_rabbit._server_details["USERNAME"] == test_config["USERNAME"]
    assert test_rabbit._server_details["PASSWORD"] == test_config["PASSWORD"]


def test_given_invalid_connection_when_connecting_to_rabbit_then_check_error_messages_logged(mock_error):
    with patch("janitor.helpers.rabbit_helpers.rabbit_connection", side_effect=Exception):
        Rabbit(test_config)
        assert mock_error.has_calls(
            call(f"Exception on connecting to RabbitMQ: {Exception}"),
        )


def test_given_valid_connection_when_closing_connection_then_check_correct_messages_logged(mock_info):
    with patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock):
        test_rabbit = Rabbit(test_config)
        test_rabbit.close()

        assert mock_info.has_calls(
            call("Closing connection to RabbitMQ..."),
        )


@patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock, return_value={"connection": None})
def test_given_invalid_connection_when_publishing_to_rabbit_then_check_error_messages_logged(mock_error):
    with patch("janitor.rabbitmq.publisher.Publisher.publish_message") as mock_publish:
        test_rabbit = Rabbit(test_config)
        test_rabbit.batch_publish_messages(
            exchange=TEST_EXCHANGE, schema_filepath=TEST_SCHEMA_FILEPATH, headers={}, message_dicts=[], batch_size=1
        )

        assert mock_error.has_calls(
            call("Not connected to RabbitMQ!"),
        )

        assert mock_publish.call_count == 0


@patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock)
def test_given_no_messages_when_publishing_to_rabbit_then_check_error_messages_logged(mock_error):
    with patch("janitor.rabbitmq.publisher.Publisher.publish_message") as mock_publish:
        test_rabbit = Rabbit(test_config)
        test_rabbit.batch_publish_messages(
            exchange=TEST_EXCHANGE, schema_filepath=TEST_SCHEMA_FILEPATH, headers={}, message_dicts=[], batch_size=1
        )

        assert mock_error.has_calls(
            call("No messages to publish to RabbitMQ!"),
        )

        assert mock_publish.call_count == 0


@patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock)
def test_given_publisher_error_when_publishing_to_rabbit_then_check_error_messages_logged(mock_error):
    with patch("janitor.rabbitmq.publisher.Publisher.publish_message", side_effect=Exception):
        test_rabbit = Rabbit(test_config)
        test_rabbit.batch_publish_messages(
            exchange=TEST_EXCHANGE,
            schema_filepath=TEST_SCHEMA_FILEPATH,
            headers={},
            message_dicts=TEST_MESSAGES,
            batch_size=TEST_BATCH_SIZE,
        )

        assert mock_error.has_calls(
            call(f"Exception on publishing to RabbitMQ: {Exception}"),
            call("Failed to publish batch."),
        )


@patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock)
def test_given_group_of_messages_when_publishing_to_rabbit_then_check_messages_published_correctly(mock_info):
    with patch("janitor.rabbitmq.publisher.Publisher.publish_message") as mock_publish:
        test_rabbit = Rabbit(test_config)
        test_rabbit.batch_publish_messages(
            exchange=TEST_EXCHANGE,
            schema_filepath=TEST_SCHEMA_FILEPATH,
            headers={},
            message_dicts=TEST_MESSAGES,
            batch_size=TEST_BATCH_SIZE,
        )

        assert mock_publish.has_calls(
            call({}, TEST_MESSAGES[:2]),
            call({}, TEST_MESSAGES[2:4]),
        )

        assert mock_info.has_calls(
            call(f"Publishing messages to exchange: {TEST_EXCHANGE}"),
            call(f"Publishing messages in batches of size {TEST_BATCH_SIZE}"),
            call(f"Published {len(TEST_MESSAGES)} messages!"),
        )
