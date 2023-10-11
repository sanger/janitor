from typing import List, Optional
from unittest.mock import call

import pytest
from mysql.connector.errors import DatabaseError

from janitor.db.database import Database
from janitor.helpers.mysql_helpers import parse_entry
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from tests.data.entries import Entries
from tests.types import (
    AuditsTableEntry,
    CoordinatesTableEntry,
    LabwareLocationTableEntry,
    LabwaresTableEntry,
    LocationsTableEntry,
    UsersTableEntry,
)

labware_location_columns = [
    "id",
    "labware_barcode",
    "location_barcode",
    "full_location_address",
    "coordinate_position",
    "coordinate_row",
    "coordinate_column",
    "lims_id",
    "stored_by",
    "stored_at",
    "created_at",
    "updated_at",
]

test_entries = Entries()


def write_to_tables(
    lw_database: Database,
    mlwh_database: Database,
    labwares_entries: Optional[List[LabwaresTableEntry]] = None,
    audits_entries: Optional[List[AuditsTableEntry]] = None,
    users_entries: Optional[List[UsersTableEntry]] = None,
    locations_entries: Optional[List[LocationsTableEntry]] = None,
    coordinates_entries: Optional[List[CoordinatesTableEntry]] = None,
    labware_location_entries: Optional[List[LabwareLocationTableEntry]] = None,
) -> None:
    """
    Write entries to the tables in the LabWhere and MLWH databases.

    Parameters:
        lw_database {Database}: LabWhere database
        mlwh_database {Database}: MLWH database
        labwares_entries {List[LabwaresTableEntry]}: Entries for labwares table (optional)
        audits_entries {List[AuditsTableEntry]}: Entries for audits table (optional)
        users_entries {List[UsersTableEntry]}: Entries for users table (optional)
        locations_entries {List[LocationsTableEntry]}: Entries for locations table (optional)
        coordinates_entries {List[CoordinatesTableEntry]}: Entries for coordinates table (optional)
        labware_location_entries {List[LabwareLocationTableEntry]}: Entries for labware_location table (optional)
    """
    if labwares_entries:
        insert_into_table_query = (
            "INSERT INTO labwares (id, barcode, location_id, coordinate_id) VALUES (%s, %s, %s, %s);"
        )
        lw_database.write_entries_to_table(insert_into_table_query, labwares_entries, len(labwares_entries))

    if audits_entries:
        insert_into_table_query = """
        INSERT INTO audits (id, auditable_id, auditable_type, user_id, updated_at) VALUES (%s, %s, %s, %s, %s);
        """
        lw_database.write_entries_to_table(insert_into_table_query, audits_entries, len(audits_entries))

    if users_entries:
        insert_into_table_query = "INSERT INTO users (id, login) VALUES (%s, %s);"
        lw_database.write_entries_to_table(insert_into_table_query, users_entries, len(users_entries))

    if locations_entries:
        insert_into_table_query = "INSERT INTO locations (id, barcode, parentage) VALUES (%s, %s, %s);"
        lw_database.write_entries_to_table(insert_into_table_query, locations_entries, len(locations_entries))

    if coordinates_entries:
        insert_into_table_query = (
            "INSERT INTO coordinates (id, `position`, `row`, `column`, location_id) VALUES (%s, %s, %s, %s, %s);"
        )
        lw_database.write_entries_to_table(insert_into_table_query, coordinates_entries, len(coordinates_entries))

    if labware_location_entries:
        insert_into_table_query = """
                INSERT INTO labware_location
                (
                    id,
                    labware_barcode,
                    location_barcode,
                    full_location_address,
                    coordinate_position,
                    coordinate_row,
                    coordinate_column,
                    lims_id,
                    stored_by,
                    stored_at,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        mlwh_database.write_entries_to_table(
            insert_into_table_query, labware_location_entries, len(labware_location_entries)
        )


def test_given_valid_db_details_when_connecting_to_db_then_check_connection_successful(
    mock_info, config, mlwh_database
):
    sync_changes_from_labwhere(config)

    assert mock_info.has_calls(
        [
            call("[DATABASE_CONNECTION]"),
            call("[DATABASE_CONNECTION]"),
            call("[DATABASE_CONNECTION]"),
            call("[DATABASE_CONNECTION]"),
        ]
    )


def test_given_valid_connection_and_deleting_db_when_attempting_sync_then_check_exception_raised(
    mock_error, config, mlwh_database
):
    mlwh_database.execute_query(f"DROP DATABASE {config.MLWH_DB['db_name']}", {})
    with pytest.raises(DatabaseError):
        sync_changes_from_labwhere(config)

    assert mock_error.has_calls([call("[TASK_EXCEPTION]")])


def test_given_valid_connection_and_deleting_labware_location_table_when_attempting_sync_then_check_exception_raised(
    mock_error, config, mlwh_database
):
    mlwh_database.execute_query("DROP TABLE labware_location", {})
    with pytest.raises(IndexError):
        sync_changes_from_labwhere(config)

    assert mock_error.has_calls([call("[TASK_EXCEPTION]")])


def test_given_good_input_entry_with_location_when_making_mlwh_entry_then_check_entry_written_correctly(
    mock_info, mock_error, config, lw_database, mlwh_database, freezer
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.good_input_entry_with_location_input["labwares"],
        audits_entries=test_entries.good_input_entry_with_location_input["audits"],
        users_entries=test_entries.good_input_entry_with_location_input["users"],
        locations_entries=test_entries.good_input_entry_with_location_input["locations"],
    )
    sync_changes_from_labwhere(config)

    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = test_entries.good_input_entry_with_location_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"] == expected_result["stored_at"]
    assert actual_result["created_at"] == expected_result["created_at"]
    assert actual_result["updated_at"] == expected_result["updated_at"]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.call_count == 0


def test_given_good_input_entry_with_coordinates_when_making_mlwh_entry_then_check_entry_written_correctly(
    mock_info, mock_error, config, lw_database, mlwh_database, freezer
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.good_input_entry_with_coordinates_input["labwares"],
        audits_entries=test_entries.good_input_entry_with_coordinates_input["audits"],
        users_entries=test_entries.good_input_entry_with_coordinates_input["users"],
        locations_entries=test_entries.good_input_entry_with_coordinates_input["locations"],
        coordinates_entries=test_entries.good_input_entry_with_coordinates_input["coordinates"],
    )
    sync_changes_from_labwhere(config)

    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = test_entries.good_input_entry_with_coordinates_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"] == expected_result["stored_at"]
    assert actual_result["created_at"] == expected_result["created_at"]
    assert actual_result["updated_at"] == expected_result["updated_at"]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.call_count == 0


def test_given_good_input_entry_with_two_audits_when_making_mlwh_entry_then_check_latest_audit_used(
    mock_info, mock_error, config, lw_database, mlwh_database, freezer
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.good_input_entry_with_two_audits_input["labwares"],
        audits_entries=test_entries.good_input_entry_with_two_audits_input["audits"],
        users_entries=test_entries.good_input_entry_with_two_audits_input["users"],
        locations_entries=test_entries.good_input_entry_with_two_audits_input["locations"],
    )
    sync_changes_from_labwhere(config)

    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = test_entries.good_input_entry_with_two_audits_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"] == expected_result["stored_at"]
    assert actual_result["created_at"] == expected_result["created_at"]
    assert actual_result["updated_at"] == expected_result["updated_at"]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.call_count == 0


def test_given_good_input_entry_outdated_record_in_mlwh_when_checking_entries_then_check_entry_updated_correctly(
    mock_info, mock_error, config, lw_database, mlwh_database, freezer
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.good_input_entry_outdated_record_in_mlwh_input["labwares"],
        audits_entries=test_entries.good_input_entry_outdated_record_in_mlwh_input["audits"],
        users_entries=test_entries.good_input_entry_outdated_record_in_mlwh_input["users"],
        locations_entries=test_entries.good_input_entry_outdated_record_in_mlwh_input["locations"],
        labware_location_entries=test_entries.good_input_entry_outdated_record_in_mlwh_input["labware_location"],
    )
    sync_changes_from_labwhere(config)

    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = test_entries.good_input_entry_outdated_record_in_mlwh_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"] == expected_result["stored_at"]
    assert actual_result["created_at"] == expected_result["created_at"]
    assert actual_result["updated_at"] == expected_result["updated_at"]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.call_count == 0


def test_given_bad_input_entry_without_location_when_making_sorting_entries_then_check_entry_filtered_out(
    mock_info, mock_error, config, lw_database, mlwh_database
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.bad_input_entry_without_location_input["labwares"],
        audits_entries=test_entries.bad_input_entry_without_location_input["audits"],
        users_entries=test_entries.bad_input_entry_without_location_input["users"],
    )
    sync_changes_from_labwhere(config)

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.has_calls(
        [
            call("TASK_ERROR"),
            call(f"Found invalid entry: {test_entries.bad_input_entry_without_location_input['labwares'][0]}"),
        ]
    )


def test_given_bad_input_entry_without_audits_when_sorting_entries_then_check_entry_filtered_out(
    mock_info, mock_error, config, lw_database, mlwh_database
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.bad_input_entry_without_audits_input["labwares"],
        locations_entries=test_entries.bad_input_entry_without_audits_input["locations"],
    )
    sync_changes_from_labwhere(config)

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.has_calls(
        [
            call("TASK_ERROR"),
            call(f"Found invalid entry: {test_entries.bad_input_entry_without_audits_input['labwares'][0]}"),
        ]
    )


def test_given_bad_input_entry_without_location_without_audits_when_sorting_entries_then_check_entry_filtered_out(
    mock_info, mock_error, config, lw_database, mlwh_database
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.bad_input_entry_without_location_without_audits_input["labwares"],
    )
    sync_changes_from_labwhere(config)

    bad_entry = test_entries.bad_input_entry_without_location_without_audits_input["labwares"][0]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.has_calls([call("TASK_ERROR"), call(f"Found invalid entry: {bad_entry}")])


def test_given_mixed_entries_when_writing_entries_then_check_all_entries_processed_correctly(
    mock_info, mock_error, config, lw_database, mlwh_database, freezer
):
    write_to_tables(
        lw_database,
        mlwh_database,
        labwares_entries=test_entries.mixed_entries_input["labwares"],
        audits_entries=test_entries.mixed_entries_input["audits"],
        users_entries=test_entries.mixed_entries_input["users"],
        locations_entries=test_entries.mixed_entries_input["locations"],
        coordinates_entries=test_entries.mixed_entries_input["coordinates"],
    )
    sync_changes_from_labwhere(config)

    good_entries = mlwh_database.execute_query("SELECT * FROM labware_location", {})
    for result_index in range(len(good_entries)):
        actual_result = parse_entry(good_entries[result_index], labware_location_columns)
        expected_result = test_entries.mixed_entries_output["labware_location"][result_index]

        assert actual_result["id"] == expected_result["id"]
        assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
        assert actual_result["location_barcode"] == expected_result["location_barcode"]
        assert actual_result["full_location_address"] == expected_result["full_location_address"]
        assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
        assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
        assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
        assert actual_result["lims_id"] == expected_result["lims_id"]
        assert actual_result["stored_by"] == expected_result["stored_by"]
        assert actual_result["stored_at"] == expected_result["stored_at"]
        assert actual_result["created_at"] == expected_result["created_at"]
        assert actual_result["updated_at"] == expected_result["updated_at"]

    assert mock_info.has_calls([call("TASK_START"), call("TASK_PROGRESS"), call("TASK_PROGRESS"), call("TASK_SUCCESS")])

    assert mock_error.has_calls(
        [
            call("TASK_ERROR"),
            call(f"Found invalid entry: {test_entries.mixed_entries_input['labwares'][1]}"),
            call("TASK_ERROR"),
            call(f"Found invalid entry: {test_entries.mixed_entries_input['labwares'][3]}"),
            call("TASK_ERROR"),
            call(f"Found invalid entry: {test_entries.mixed_entries_input['labwares'][5]}"),
        ]
    )
