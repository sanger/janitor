from datetime import datetime
from typing import Any, List, Optional
from unittest.mock import call, patch

import pytest
from mysql.connector.errors import DatabaseError

from janitor.db.database import Database
from janitor.helpers.mlwh_helpers import make_sample_sequence_message_dicts
from janitor.tasks.sequencing_publisher.main import get_and_publish_sequencing_run_status_changes
from janitor.types import SampleSequenceMessage
from tests.data.sequencing_publisher_entries import Entries
from tests.types import (
    EventsTableEntry,
    EventTypesTableEntry,
    IseqFlowcellTableEntry,
    IseqProductMetricsTableEntry,
    IseqRunStatusTableEntry,
    RolesTableEntry,
    RoleTypesTableEntry,
    SampleTableEntry,
    SeqProductsIrodsLocationsTableEntry,
    StudyTableEntry,
    SubjectsTableEntry,
)

run_status_columns = [
    "change_date",
    "id_run",
    "sequencing_study",
    "sample_supplier_id",
    "labware_barcode",
    "run_status",
    "irods_root_collection",
    "irods_data_relative_path",
    "irods_secondary_data_relative_path",
    "latest_timestamp",
]

test_entries = Entries()


def write_to_table(database: Database, insert_into_table_query: str, entries: List[Any]) -> None:
    """
    Write entries to table.

    Parameters:
        database {Database}: Database containing table
        insert_into_table_query {str}: SQL query for inserting into table
        entries {List[Any]}: Entries to write to table
    """
    database.write_entries_to_table(insert_into_table_query, entries, len(entries))


def write_to_mlwh_database(
    mlwh_database: Database,
    iseq_flowcell_entries: Optional[List[IseqFlowcellTableEntry]] = None,
    iseq_product_metrics_entries: Optional[List[IseqProductMetricsTableEntry]] = None,
    iseq_run_status_entries: Optional[List[IseqRunStatusTableEntry]] = None,
    sample_entries: Optional[List[SampleTableEntry]] = None,
    seq_product_irods_locations_entries: Optional[List[SeqProductsIrodsLocationsTableEntry]] = None,
    study_entries: Optional[List[StudyTableEntry]] = None,
) -> None:
    """
    Write entries to the tables in the MLWH database.

    Parameters:
        mlwh_database {Database}: MLWH database
        iseq_flowcell_entries {List[IseqFlowcellTableEntry]}: Entries for users table (optional)
        iseq_product_metrics_entries {List[IseqProductMetricsTableEntry]}: Entries for locations table (optional)
        iseq_run_status_entries {List[IseqRunStatusTableEntry]}: Entries for coordinates table (optional)
        sample_entries {List[SampleTableEntry]}: Entries for labware_location table (optional)
        seq_product_irods_locations_entries {List[SeqProductsIrodsLocationsTableEntry]}: Entries for labware_location
        table (optional)
        study_entries {List[StudyTableEntry]}: Entries for labware_location table (optional)
    """
    if iseq_flowcell_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO iseq_flowcell (id_iseq_flowcell_tmp, id_sample_tmp, id_study_tmp) VALUES (%s, %s, %s);
            """,
            entries=iseq_flowcell_entries,
        )

    if iseq_product_metrics_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO iseq_product_metrics (id_iseq_product, id_iseq_flowcell_tmp, id_run) VALUES (%s, %s, %s);
            """,
            entries=iseq_product_metrics_entries,
        )

    if iseq_run_status_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO iseq_run_status (id_run, date, id_run_status_dict) VALUES (%s, %s, %s);
            """,
            entries=iseq_run_status_entries,
        )

    if sample_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO sample (id_sample_tmp, uuid_sample_lims, supplier_name) VALUES (%s, %s, %s);
            """,
            entries=sample_entries,
        )

    if seq_product_irods_locations_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO seq_product_irods_locations (id_product, irods_root_collection, irods_data_relative_path, \
                    irods_secondary_data_relative_path) VALUES (%s, %s, %s, %s);
            """,
            entries=seq_product_irods_locations_entries,
        )

    if study_entries:
        write_to_table(
            database=mlwh_database,
            insert_into_table_query="""
                INSERT INTO study (id_study_tmp, name) VALUES (%s, %s);
            """,
            entries=study_entries,
        )


def write_to_mlwh_events_database(
    mlwh_events_database: Database,
    events_entries: Optional[List[EventsTableEntry]] = None,
    event_types_entries: Optional[List[EventTypesTableEntry]] = None,
    roles_entries: Optional[List[RolesTableEntry]] = None,
    role_types_entries: Optional[List[RoleTypesTableEntry]] = None,
    subjects_entries: Optional[List[SubjectsTableEntry]] = None,
) -> None:
    """
    Write entries to the tables in the MLWH events database.

    Parameters:
        mlwh_events_database {Database}: MLWH events database
        events_entries {List[EventsTableEntry]}: Entries for audits table (optional)
        event_types_entries {List[EventTypesTableEntry]}: Entries for labwares table (optional)
        roles_entries {List[RolesTableEntry]}: Entries for labware_location table (optional)
        role_types_entries {List[RoleTypesTableEntry]}: Entries for labware_location table (optional)
        subjects_entries {List[SubjectsTableEntry]}: Entries for labware_location table (optional)
    """
    if events_entries:
        write_to_table(
            database=mlwh_events_database,
            insert_into_table_query="""
                INSERT INTO events (id, event_type_id, occured_at) VALUES (%s, %s, %s);
            """,
            entries=events_entries,
        )

    if event_types_entries:
        write_to_table(
            database=mlwh_events_database,
            insert_into_table_query="""
                INSERT INTO event_types (id, `key`) VALUES (%s, %s);
            """,
            entries=event_types_entries,
        )

    if roles_entries:
        write_to_table(
            database=mlwh_events_database,
            insert_into_table_query="""
                INSERT INTO roles (event_id, role_type_id, subject_id) VALUES (%s, %s, %s);
            """,
            entries=roles_entries,
        )

    if role_types_entries:
        write_to_table(
            database=mlwh_events_database,
            insert_into_table_query="""
                INSERT INTO role_types (id, `key`) VALUES (%s, %s);
            """,
            entries=role_types_entries,
        )

    if subjects_entries:
        write_to_table(
            database=mlwh_events_database,
            insert_into_table_query="""
                INSERT INTO subjects (id, uuid, friendly_name) VALUES (%s, %s, %s);
            """,
            entries=subjects_entries,
        )


@patch("janitor.rabbitmq.rabbit.Rabbit.batch_publish_messages", return_value=None)
@patch("janitor.helpers.mlwh_helpers.make_sample_sequence_message_dicts")
def test_given_test_data_in_databases_when_querying_database_then_check_correct_rows_returned(
    mock_publish, mock_make_messages, mock_error, config, mlwh_database, mlwh_events_database, mock_rabbit
):
    write_to_mlwh_database(
        mlwh_database=mlwh_database,
        iseq_flowcell_entries=test_entries.good_input_entry["iseq_flowcell"],
        iseq_product_metrics_entries=test_entries.good_input_entry["iseq_product_metrics"],
        iseq_run_status_entries=test_entries.good_input_entry["iseq_run_status"],
        sample_entries=test_entries.good_input_entry["sample"],
        seq_product_irods_locations_entries=test_entries.good_input_entry["seq_product_irods_locations"],
        study_entries=test_entries.good_input_entry["study"],
    )

    write_to_mlwh_events_database(
        mlwh_events_database=mlwh_events_database,
        events_entries=test_entries.good_input_entry["events"],
        event_types_entries=test_entries.good_input_entry["event_types"],
        roles_entries=test_entries.good_input_entry["roles"],
        role_types_entries=test_entries.good_input_entry["role_types"],
        subjects_entries=test_entries.good_input_entry["subjects"],
    )

    expected_message_dicts = [
        SampleSequenceMessage(
            change_date=datetime(2023, 9, 11, 9, 10, 43),
            id_run=47819,
            sequencing_study="sequencing_study",
            sample_supplier_id="sample_supplier_id",
            labware_barcode="labware_barcode",
            run_status=1,
            irods_root_collection="root_collection",
            irods_data_relative_path="data_relative",
            irods_secondary_data_relative_path=None,
            latest_timestamp=datetime(2023, 9, 11, 9, 10, 43),
        )
    ]

    with patch("janitor.helpers.log_helpers.load_job_timestamp") as mock_latest_timestamp:
        mock_latest_timestamp.return_value = None
        get_and_publish_sequencing_run_status_changes(config)
        assert mock_make_messages.has_calls(call(expected_message_dicts))

    assert mock_error.call_count == 0


def test_given_valid_db_details_when_no_updates_in_database_then_check_exits_early(
    mock_info, mock_error, config, mlwh_database, mlwh_events_database
):
    with patch("janitor.db.database.Database.execute_query") as mock_execute:
        mock_execute.return_value = []
        get_and_publish_sequencing_run_status_changes(config)

    assert mock_info.has_calls([call("TASK_COMPLETE"), call("No new changes from MLWH. Skipping task...")])

    assert mock_error.call_count == 0


@patch("janitor.db.database.Database.execute_query", side_effect=DatabaseError())
def test_given_error_when_querying_database_then_check_task_fails(mock_error, config):
    with pytest.raises(DatabaseError):
        get_and_publish_sequencing_run_status_changes(config)

    assert mock_error.has_calls([call("[TASK_EXCEPTION]"), call("[TASK_FAILED]")])


@patch("janitor.rabbitmq.rabbit.Rabbit.batch_publish_messages", return_value=None)
def test_given_one_entry_returned_when_querying_database_then_check_correct_message_published(
    mock_publish, mock_info, mock_error, mock_rabbit, config
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

    assert mock_info.has_calls([call("[TASK_PROGRESS]"), call("[TASK_SUCCESS]")])

    assert mock_publish.has_calls(
        call(
            config.RABBITMQ_SEQUENCING_EXCHANGE,
            config.RABBITMQ_SEQUENCING_MESSAGE_SCHEMA,
            {},
            test_message_dicts,
            config.SEQUENCING_PUBLISHER_MESSAGES_BATCH_SIZE,
        )
    )

    assert mock_error.call_count == 0


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

    assert mock_error.has_calls([call("[TASK_FAILED]")])
