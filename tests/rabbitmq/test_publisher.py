from unittest.mock import PropertyMock, call, mock_open, patch

from pika import BasicProperties, BlockingConnection

from janitor.rabbitmq.publisher import Publisher

TEST_EXCHANGE = "test_exchange"
TEST_SCHEMA_FILE = "test/schema/file"
TEST_SCHEMA = "test_schema"


def test_given_publisher_details_when_creating_publisher_then_check_publisher_has_correct_parameters(mock_rabbit):
    test_publisher = Publisher(mock_rabbit.connection, TEST_EXCHANGE, TEST_SCHEMA_FILE)

    assert test_publisher._connection == mock_rabbit.connection
    assert test_publisher._exchange == TEST_EXCHANGE
    assert test_publisher._schema_filepath == TEST_SCHEMA_FILE


@patch("janitor.rabbitmq.publisher.parse_schema")
@patch("json.load")
def test_given_schema_filepath_when_creating_schema_then_check_schema_created_using_file(
    mock_parse_schema, mock_json_load, mock_rabbit
):
    test_publisher = Publisher(mock_rabbit.connection, TEST_EXCHANGE, TEST_SCHEMA_FILE)
    mock_json_load.return_value = "schema"

    with patch("builtins.open", mock_open(read_data=TEST_SCHEMA)):
        assert test_publisher.schema == "schema"
        assert mock_json_load.has_calls(call(TEST_SCHEMA))
        assert mock_parse_schema.has_calls(call("schema"))


@patch("janitor.rabbitmq.publisher.json_writer")
def test_given_no_schema_when_serialising_message_then_check_message_not_serialised(mock_json_writer, mock_rabbit):
    test_publisher = Publisher(mock_rabbit.connection, TEST_EXCHANGE, TEST_SCHEMA_FILE)
    test_message_dicts = [{"message": 1}, {"message": 2}, {"message": 3}]

    with patch("janitor.rabbitmq.publisher.Publisher.schema", new_callable=PropertyMock) as mock_schema:
        mock_schema.return_value = None

        serialised_message = test_publisher.serialise_message(test_message_dicts)

        assert mock_json_writer.call_count == 0
        assert serialised_message == ""


@patch("io.StringIO")
@patch("janitor.rabbitmq.publisher.json_writer")
def test_given_schema_when_serialising_message_then_check_message_serialised(
    mock_string_io, mock_json_writer, mock_rabbit
):
    test_publisher = Publisher(mock_rabbit.connection, TEST_EXCHANGE, TEST_SCHEMA_FILE)
    test_message_dicts = [{"message": 1}, {"message": 2}, {"message": 3}]

    with patch("janitor.rabbitmq.publisher.Publisher.schema", new_callable=PropertyMock) as mock_schema:
        test_publisher.serialise_message(test_message_dicts)
        assert mock_json_writer.has_calls(call(mock_string_io, mock_schema, test_message_dicts))


@patch("pika.BlockingConnection", spec=BlockingConnection)
def test_given_messages_when_publishing_then_check_publisher_called_with_correct_parameters(
    mock_blocking_connection, mock_rabbit
):
    test_publisher = Publisher(mock_rabbit._connection, TEST_EXCHANGE, TEST_SCHEMA_FILE)
    test_headers = {"header": "header"}
    test_message_dicts = [{"message": 1}, {"message": 2}, {"message": 3}]
    test_routing_key = "routing_key"

    with patch("janitor.rabbitmq.publisher.Publisher.serialise_message") as mock_serialise_message:
        test_publisher.publish_message(
            headers=test_headers, message_dicts=test_message_dicts, routing_key=test_routing_key
        )
        mock_serialise_message.return_value = "messages"
        assert mock_serialise_message.has_calls(call(test_message_dicts))
        assert mock_rabbit._connection.return_value.channel.return_value.basic_publish.has_calls(
            call(
                exchange=TEST_EXCHANGE,
                routing_key=test_routing_key,
                properties=BasicProperties(str(test_headers)),
                body="messages",
            ),
        )
