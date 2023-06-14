import datetime
from typing import List, Dict


def load_query(filepath: str) -> str:
    """Load query from .sql file.

    Arguments:
        filepath {str}: filepath to .sql file with query

    Returns:
        {str}: SQL query from .sql file
    """
    with open(filepath, "r") as query:
        return query.read()


def parse_result(result: List, column_names: List[str]) -> Dict[str, str | int]:
    """Parse result into dictionary form for easier indexing.

    Arguments:
        result {List}: data to assign column names to
        column_names {List[str]}: list of column names corresponding to results

    Returns:
        {Dict[str, str | int]}: dictionary of column names and corresponding data
    """
    return dict(zip(column_names, result))


def make_mlwh_entry(entry: Dict[str, str | int]):
    """Make MLWH entry from results to write to table.

    Arguments:
        entry {Dict[str, str | int]}: parsed entry to write to table

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
    created_at = datetime.datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    updated_at = datetime.datetime.utcnow().isoformat(sep=" ", timespec="seconds")

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
