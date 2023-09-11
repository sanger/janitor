from datetime import datetime
from unittest.mock import call, patch

import pytest
from mysql.connector.errors import DatabaseError

from janitor.helpers.mlwh_helpers import make_sample_sequence_message_dicts
from janitor.tasks.sequencing_publisher.main import get_and_publish_sequencing_run_status_changes
from janitor.types import SampleSequenceMessage


def test_given_valid_db_details_when_no_updates_in_database_then_check_exits_early(
    mock_info, mock_error, config, mlwh_database, mlwh_events_database
):
    with patch("janitor.db.database.Database.execute_query") as mock_execute:
        mock_execute.return_value = []
        get_and_publish_sequencing_run_status_changes(config)

    assert mock_info.has_calls(
        call("Starting sequencing publisher task..."),
        call("Closing connections to databases..."),
        call("No new changes from MLWH. Skipping task..."),
    )

    assert mock_error.call_count == 0


@patch("janitor.db.database.Database.execute_query", side_effect=DatabaseError())
def test_given_error_when_querying_database_then_check_task_fails(mock_error, config):
    with pytest.raises(DatabaseError):
        get_and_publish_sequencing_run_status_changes(config)

    assert mock_error.has_calls(
        call(f"Exception on querying database: {DatabaseError()}"),
        call("Task failed!"),
    )


@patch("janitor.rabbitmq.rabbit.Rabbit.batch_publish_messages", return_value=None)
def test_given_one_entry_returned_when_querying_database_then_check_correct_message_published(
    mock_publish, mock_info, mock_rabbit, config
):
    test_message_dicts = make_sample_sequence_message_dicts(
        [
            SampleSequenceMessage(
                change_date=datetime(year=2023, month=9, day=7),
                id_run=1,
                sequencing_study="study",
                sample_supplier_id="supplier_id",
                labware_barcode="barcode",
                run_status=1,
                irods_root_collection="root_collection",
                irods_data_relative_path=None,
                irods_secondary_data_relative_path=None,
                latest_timestamp=datetime(year=2023, month=9, day=7),
            )
        ]
    )

    with patch("janitor.db.database.Database.execute_query") as mock_execute:
        test_query_return = [
            datetime(year=2023, month=9, day=7),
            1,
            "study",
            "supplier_id",
            "barcode",
            1,
            "root_collection",
            None,
            None,
        ]
        mock_execute.return_value = [test_query_return]
        get_and_publish_sequencing_run_status_changes(config)

    assert mock_info.has_calls(
        call("Number of changes to publish: 1"),
        call("Task successful!"),
    )

    assert mock_publish.has_calls(
        call(
            config.RABBITMQ_SEQUENCING_EXCHANGE,
            config.RABBITMQ_SEQUENCING_MESSAGE_SCHEMA,
            {},
            test_message_dicts,
            config.SEQUENCING_PUBLISHER_MESSAGES_BATCH_SIZE,
        )
    )


@patch("janitor.helpers.log_helpers.save_job_timestamp")
@patch("janitor.rabbitmq.rabbit.Rabbit.batch_publish_messages")
@patch("janitor.db.database.Database.execute_query")
def test_given_error_when_publishing_to_rabbit_then_check_task_fails(
    mock_execute, mock_publish, mock_save_timestamp, mock_error, mock_rabbit, config
):
    test_message_dicts = make_sample_sequence_message_dicts(
        [
            SampleSequenceMessage(
                change_date=datetime(year=2023, month=9, day=7),
                id_run=1,
                sequencing_study="study",
                sample_supplier_id="supplier_id",
                labware_barcode="barcode",
                run_status=1,
                irods_root_collection="root_collection",
                irods_data_relative_path=None,
                irods_secondary_data_relative_path=None,
                latest_timestamp=datetime(year=2023, month=9, day=7),
            )
        ]
    )

    mock_publish.return_value = test_message_dicts

    test_query_return = [
        datetime(year=2023, month=9, day=7),
        1,
        "study",
        "supplier_id",
        "barcode",
        1,
        "root_collection",
        None,
        None,
    ]
    mock_execute.return_value = [test_query_return]

    with pytest.raises(Exception):  # noqa: B017
        get_and_publish_sequencing_run_status_changes(config)
        assert mock_save_timestamp.has_calls(
            call(config.SEQUENCING_PUBLISHER_JOB_NAME, test_message_dicts[0]["latest_timestamp"])
        )

    assert mock_error.has_calls(call("Task failed!"))
