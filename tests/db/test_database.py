from unittest.mock import call, patch

import mysql.connector
import pytest
from mysql.connector.errors import DatabaseError

from janitor.db.database import Database
from janitor.types import DbConnectionDetails

test_config = DbConnectionDetails(
    host="test_host", port=1, db_name="test_dbname", username="test_username", password="test_password"
)


def test_given_invalid_connection_when_connecting_to_db_then_check_error_messages_logged(mock_error):
    with patch("mysql.connector.connect", side_effect=mysql.connector.Error()):
        Database(test_config).connection
        assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])


def test_given_invalid_connection_when_closing_connection_then_check_error_message_logged(mock_error):
    with patch("mysql.connector.connect") as mock_connect:
        mock_connect.return_value.close.return_value = mysql.connector.Error()
        test_db = Database(test_config)
        test_db.close()
        assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])


def test_given_valid_connection_details_when_connection_fails_then_check_error_message_logged(mock_error, config):
    with patch("mysql.connector.connect") as mock_connect:
        mock_connect.return_value.is_connected.return_value = False
        test_db = Database(test_config)

        assert test_db.connection is None
        assert mock_error.has_calls([call("[DATABASE_ERROR]")])


def test_given_error_when_executing_sql_query_then_check_error_message_logged(mock_error, config):
    with patch("mysql.connector.cursor") as mock_cursor:
        mock_cursor.return_value.execute.return_value = DatabaseError("Error executing query")
        test_db = Database(config.MLWH_DB)
        test_db.execute_query("query", {})
        assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])


def test_given_no_db_connection_when_executing_query_then_check_error_message_logged(mock_error):
    with pytest.raises(DatabaseError):
        test_db = Database(test_config)
        test_db.execute_query("query", {})

    assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])


def test_given_error_when_writing_to_table_then_check_error_message_logged(mock_error, config):
    with patch("mysql.connector.cursor") as mock_cursor:
        mock_cursor.return_value.executemany.return_value = AttributeError("Database not connected")
        test_db = Database(config.MLWH_DB)
        test_db.write_entries_to_table("query", [], 5000)
        assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])


def test_given_no_db_connection_when_writing_to_table_then_check_error_message_logged(mock_error):
    with pytest.raises(DatabaseError):
        test_db = Database(test_config)
        test_db.write_entries_to_table("query", [], 5000)

    assert mock_error.has_calls([call("[DATABASE_EXCEPTION]")])
