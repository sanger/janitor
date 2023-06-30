from unittest.mock import call, patch

import pytest

from janitor.helpers.mysql_helpers import parse_entry
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from tests.data.entries import (
    bad_input_entry_without_audits_input,
    bad_input_entry_without_location_input,
    bad_input_entry_without_location_without_audits_input,
    good_input_entry_outdated_record_in_mlwh_input,
    good_input_entry_outdated_record_in_mlwh_output,
    good_input_entry_with_coordinates_input,
    good_input_entry_with_coordinates_output,
    good_input_entry_with_location_input,
    good_input_entry_with_location_output,
    good_input_entry_with_two_audits_input,
    good_input_entry_with_two_audits_output,
    mixed_entries_input,
    mixed_entries_output,
)


@patch("logging.info")
def test_given_valid_db_details_when_connecting_to_db_then_check_connection_successful(
    mock_info,
    config,
):
    sync_changes_from_labwhere(config)
    assert mock_info.has_calls(
        call(f"Attempting to connect to {config.LABWHERE_DB['host']} on port {config.LABWHERE_DB['host']}..."),
        call(f"MySQL connection to {config.LABWHERE_DB['db_name']} successful!"),
        call(f"Attempting to connect to {config.MLWH_DB['host']} on port {config.MLWH_DB['host']}..."),
        call(f"MySQL connection to {config.MLWH_DB['db_name']} successful!"),
    )


@pytest.mark.parametrize(
    "lw_labwares_table",
    [good_input_entry_with_location_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [good_input_entry_with_location_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [good_input_entry_with_location_input["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [good_input_entry_with_location_input["locations"]],
    indirect=True,
)
@patch("logging.info")
def test_given_good_input_entry_with_location_id_when_making_mlwh_entry_then_check_entry_written_correctly(
    mock_info,
    config,
    mlwh_database,
    mlwh_labware_locations_table,
    labware_location_columns,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = good_input_entry_with_location_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"].minute == expected_result["stored_at"].minute
    assert actual_result["created_at"].minute == expected_result["created_at"].minute
    assert actual_result["updated_at"].minute == expected_result["updated_at"].minute

    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 1 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )


@pytest.mark.parametrize(
    "lw_labwares_table",
    [good_input_entry_with_coordinates_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [good_input_entry_with_coordinates_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [good_input_entry_with_coordinates_input["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [good_input_entry_with_coordinates_input["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [good_input_entry_with_coordinates_input["coordinates"]],
    indirect=True,
)
@patch("logging.info")
def test_given_good_input_entry_with_coordinate_id_when_making_mlwh_entry_then_check_entry_written_correctly(
    mock_info,
    config,
    mlwh_database,
    mlwh_labware_locations_table,
    labware_location_columns,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = good_input_entry_with_coordinates_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"].minute == expected_result["stored_at"].minute
    assert actual_result["created_at"].minute == expected_result["created_at"].minute
    assert actual_result["updated_at"].minute == expected_result["updated_at"].minute

    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 1 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )


@pytest.mark.parametrize(
    "lw_labwares_table",
    [good_input_entry_with_two_audits_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [good_input_entry_with_two_audits_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [good_input_entry_with_two_audits_input["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [good_input_entry_with_two_audits_input["locations"]],
    indirect=True,
)
@patch("logging.info")
def test_given_good_input_entry_with_two_audits_when_making_mlwh_entry_then_check_latest_audit_used(
    mock_info,
    config,
    mlwh_database,
    mlwh_labware_locations_table,
    labware_location_columns,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = good_input_entry_with_two_audits_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"].minute == expected_result["stored_at"].minute
    assert actual_result["created_at"].minute == expected_result["created_at"].minute
    assert actual_result["updated_at"].minute == expected_result["updated_at"].minute

    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 1 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )


@pytest.mark.parametrize(
    "mlwh_labware_locations_table",
    [good_input_entry_outdated_record_in_mlwh_output["labware_location"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [good_input_entry_outdated_record_in_mlwh_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [good_input_entry_outdated_record_in_mlwh_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [good_input_entry_outdated_record_in_mlwh_input["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [good_input_entry_outdated_record_in_mlwh_input["locations"]],
    indirect=True,
)
@patch("logging.info")
def test_given_good_outdated_entry_in_mlwh_when_checking_entries_then_check_entry_updated_correctly(
    mock_info,
    config,
    mlwh_database,
    mlwh_labware_locations_table,
    labware_location_columns,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    result = mlwh_database.execute_query("SELECT * FROM labware_location", {})[0]
    actual_result = parse_entry(result, labware_location_columns)
    expected_result = good_input_entry_outdated_record_in_mlwh_output["labware_location"][0]

    assert actual_result["id"] == expected_result["id"]
    assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
    assert actual_result["location_barcode"] == expected_result["location_barcode"]
    assert actual_result["full_location_address"] == expected_result["full_location_address"]
    assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
    assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
    assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
    assert actual_result["lims_id"] == expected_result["lims_id"]
    assert actual_result["stored_by"] == expected_result["stored_by"]
    assert actual_result["stored_at"].minute == expected_result["stored_at"].minute
    assert actual_result["created_at"].minute == expected_result["created_at"].minute
    assert actual_result["updated_at"].minute == expected_result["updated_at"].minute

    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 1 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )


@pytest.mark.parametrize(
    "lw_labwares_table",
    [bad_input_entry_without_location_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [bad_input_entry_without_location_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [bad_input_entry_without_location_input["users"]],
    indirect=True,
)
@patch("logging.info")
@patch("logging.error")
def test_given_bad_input_entry_without_location_when_making_sorting_entries_then_check_entry_filtered_out(
    mock_info,
    mock_error,
    config,
    mlwh_labware_locations_table,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 0 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )

    bad_entry = bad_input_entry_without_location_input["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "lw_labwares_table",
    [bad_input_entry_without_audits_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [bad_input_entry_without_audits_input["locations"]],
    indirect=True,
)
@patch("logging.info")
@patch("logging.error")
def test_given_bad_input_entry_without_audits_when_sorting_entries_then_check_entry_filtered_out(
    mock_info,
    mock_error,
    config,
    mlwh_labware_locations_table,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 0 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )

    bad_entry = bad_input_entry_without_audits_input["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "lw_labwares_table",
    [bad_input_entry_without_location_without_audits_input["labwares"]],
    indirect=True,
)
@patch("logging.info")
@patch("logging.error")
def test_given_bad_input_entry_without_location_without_audits_when_sorting_entries_then_check_entry_filtered_out(
    mock_info,
    mock_error,
    config,
    mlwh_labware_locations_table,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 0 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )

    bad_entry = bad_input_entry_without_location_without_audits_input["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "lw_labwares_table",
    [mixed_entries_input["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [mixed_entries_input["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [mixed_entries_input["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [mixed_entries_input["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [mixed_entries_input["coordinates"]],
    indirect=True,
)
@patch("logging.info")
@patch("logging.error")
def test_given_mixed_entries_when_writing_entries_then_check_all_entries_processed_correctly(
    mock_info,
    mock_error,
    config,
    mlwh_database,
    mlwh_labware_locations_table,
    labware_location_columns,
    lw_labwares_table,
    lw_audits_table,
    lw_users_table,
    lw_locations_table,
    lw_coordinates_table,
):
    sync_changes_from_labwhere(config)
    good_entries = mlwh_database.execute_query("SELECT * FROM labware_location", {})
    for result_index in range(len(good_entries)):
        actual_result = parse_entry(good_entries[result_index], labware_location_columns)
        expected_result = mixed_entries_output["labware_location"][result_index]

        assert actual_result["id"] == expected_result["id"]
        assert actual_result["labware_barcode"] == expected_result["labware_barcode"]
        assert actual_result["location_barcode"] == expected_result["location_barcode"]
        assert actual_result["full_location_address"] == expected_result["full_location_address"]
        assert actual_result["coordinate_position"] == expected_result["coordinate_position"]
        assert actual_result["coordinate_row"] == expected_result["coordinate_row"]
        assert actual_result["coordinate_column"] == expected_result["coordinate_column"]
        assert actual_result["lims_id"] == expected_result["lims_id"]
        assert actual_result["stored_by"] == expected_result["stored_by"]
        assert actual_result["stored_at"].minute == expected_result["stored_at"].minute
        assert actual_result["created_at"].minute == expected_result["created_at"].minute
        assert actual_result["updated_at"].minute == expected_result["updated_at"].minute

    assert mock_info.has_calls(
        call("Starting sync labware locations task..."),
        call("Updating 4 rows..."),
        call("Closing connections to databases..."),
        call("Task successful!"),
    )

    assert mock_error.has_calls(
        call(f"Found invalid entry: {mixed_entries_input['labwares'][1]}"),
        call(f"Found invalid entry: {mixed_entries_input['labwares'][3]}"),
        call(f"Found invalid entry: {mixed_entries_input['labwares'][5]}"),
    )
