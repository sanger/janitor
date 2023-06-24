import pytest
from unittest.mock import patch, call
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from janitor.helpers.mysql_helpers import parse_entry
from tests.data.test_entries import TEST_ENTRIES


@pytest.mark.parametrize(
    "mlwh_labware_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["good_input_entry_with_location"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["good_input_entry_with_location"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["good_input_entry_with_location"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["good_input_entry_with_location"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
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
    expected_result = TEST_ENTRIES["good_input_entry_with_location"]["output_mlwh_expected"]["labware_location"][0]

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
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["good_input_entry_with_coordinates"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["good_input_entry_with_coordinates"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["good_input_entry_with_coordinates"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["good_input_entry_with_coordinates"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [TEST_ENTRIES["good_input_entry_with_coordinates"]["input_lw"]["coordinates"]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
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
    expected_result = TEST_ENTRIES["good_input_entry_with_coordinates"]["output_mlwh_expected"]["labware_location"][0]

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
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["good_input_entry_with_two_audits"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["good_input_entry_with_two_audits"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["good_input_entry_with_two_audits"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["good_input_entry_with_two_audits"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
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
    expected_result = TEST_ENTRIES["good_input_entry_with_two_audits"]["output_mlwh_expected"]["labware_location"][0]

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
    [TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["input_mlwh"]["labware_location"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
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
    expected_result = TEST_ENTRIES["good_input_entry_outdated_record_in_mlwh"]["output_mlwh_expected"][
        "labware_location"
    ][0]

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
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["bad_input_entry_without_location"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["bad_input_entry_without_location"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["bad_input_entry_without_location"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
@patch("janitor.tasks.labware_location.main.logging.error")
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

    bad_entry = TEST_ENTRIES["bad_input_entry_without_location"]["input_lw"]["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "mlwh_labware_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["bad_input_entry_without_audits"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["bad_input_entry_without_audits"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
@patch("janitor.tasks.labware_location.main.logging.error")
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

    bad_entry = TEST_ENTRIES["bad_input_entry_without_audits"]["input_lw"]["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "mlwh_labware_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["bad_input_entry_without_location_without_audits"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [[]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
@patch("janitor.tasks.labware_location.main.logging.error")
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

    bad_entry = TEST_ENTRIES["bad_input_entry_without_location_without_audits"]["input_lw"]["labwares"][0]

    assert mock_error.has_calls(call(f"Found invalid entry: {bad_entry}"))


@pytest.mark.parametrize(
    "mlwh_labware_locations_table",
    [[]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_labwares_table",
    [TEST_ENTRIES["mixed_input_entries"]["input_lw"]["labwares"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_audits_table",
    [TEST_ENTRIES["mixed_input_entries"]["input_lw"]["audits"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_users_table",
    [TEST_ENTRIES["mixed_input_entries"]["input_lw"]["users"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_locations_table",
    [TEST_ENTRIES["mixed_input_entries"]["input_lw"]["locations"]],
    indirect=True,
)
@pytest.mark.parametrize(
    "lw_coordinates_table",
    [TEST_ENTRIES["mixed_input_entries"]["input_lw"]["coordinates"]],
    indirect=True,
)
@patch("janitor.tasks.labware_location.main.logging.info")
@patch("janitor.tasks.labware_location.main.logging.error")
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
        expected_result = TEST_ENTRIES["mixed_input_entries"]["output_mlwh_expected"]["labware_location"][result_index]

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

    bad_entries = TEST_ENTRIES["mixed_input_entries"]["output_mlwh_expected"]["labware_location"]

    assert mock_error.has_calls(
        call(f"Found invalid entry: {bad_entries[0]}"),
        call(f"Found invalid entry: {bad_entries[1]}"),
        call(f"Found invalid entry: {bad_entries[2]}"),
        call(f"Found invalid entry: {bad_entries[3]}"),
    )
