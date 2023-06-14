from datetime import datetime
from typing import List, Dict
from janitor.helpers.mysql_helpers import parse_result


def make_mlwh_entry(entry: Dict[str, str]):
    """Make MLWH entry from results to write to table.

    Arguments:
        entry {Dict[str, str]}: parsed entry to write to table

    Returns:
        {List}: entry to write to MLWH table
    """
    labware_barcode = entry["labware_barcode"]
    location_barcode = entry["unordered_barcode"]
    full_location_address = entry["unordered_full"]
    coordinate_position = entry["coordinate_position"]
    coordinate_row = entry["coordinate_row"]
    coordinate_column = entry["coordinate_column"]
    lims_id = "LabWhere"
    stored_by = entry["stored_by"]
    stored_at = entry["stored_at"]
    created_at = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    updated_at = datetime.utcnow().isoformat(sep=" ", timespec="seconds")

    if entry["ordered_barcode"] is not None:
        location_barcode = entry["ordered_barcode"]
        full_location_address = entry["ordered_full"]

    return [
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
        updated_at,
    ]


def sort_results(results: List[List], column_names: List[str]):
    """Sort results to add to table and filter out entries missing location.

    Arguments:
        results {List[List]}: results to sort
        column_names {List[str]}: list of column names corresponding to results

    Returns:
        mlwh_entries {List[List]}: entries to add to MLWH table
        invalid_entries {List[List]}: filtered out entries
    """
    mlwh_entries = []
    invalid_entries = []
    for index in range(len(results)):
        result_dict = parse_result(results[index], column_names)
        if (
            result_dict["unordered_barcode"] is None
            and result_dict["ordered_barcode"] is None
        ):
            invalid_entries.append(result_dict)
        else:
            mlwh_entries.append(make_mlwh_entry(result_dict))

    return mlwh_entries, invalid_entries
