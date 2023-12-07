from datetime import datetime
from typing import Any, Sequence, cast

from janitor.helpers.mysql_helpers import parse_entry
from janitor.types import LabwareLabwhereEntry, LabwareMLWHEntry, SampleSequenceMessage

# labware_location
labware_labwhere_columns = [
    "id",
    "labware_barcode",
    "unordered_barcode",
    "unordered_full",
    "unordered_name",
    "ordered_barcode",
    "ordered_full",
    "ordered_name",
    "coordinate_position",
    "coordinate_row",
    "coordinate_column",
    "stored_by",
    "stored_at",
]


def make_mlwh_entry(entry: LabwareLabwhereEntry) -> LabwareMLWHEntry:
    """Make MLWH entry from LabWhere entries to write to table.

    Arguments:
        entry {LabwareLabwhereEntry}: parsed LabWhere entry

    Returns:
        {LabwareMLWHEntry}: entry to write to MLWH table
    """
    labware_barcode = entry["labware_barcode"]
    location_barcode = entry["unordered_barcode"]
    full_location_address = entry["unordered_full"]
    location_name = entry["unordered_name"]
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
        location_name = entry["ordered_name"]

    return {
        "labware_barcode": labware_barcode,
        "location_barcode": location_barcode,
        "full_location_address": full_location_address,
        "location_name": location_name,
        "coordinate_position": coordinate_position,
        "coordinate_row": coordinate_row,
        "coordinate_column": coordinate_column,
        "lims_id": lims_id,
        "stored_by": stored_by,
        "stored_at": stored_at,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def sort_results(
    entries: Sequence[Any],
) -> tuple:
    """Sort results to add to table and filter out entries missing location.

    Arguments:
        entries {Sequence[Any]}: entries to sort

    Returns:
        mlwh_entries {List[LabwareMLWHEntry]}: entries to add to MLWH table
        invalid_entries {List[LabwareLabwhereEntry]}: filtered out entries
    """
    mlwh_entries = []
    invalid_entries = []
    for index in range(len(entries)):
        result_dict = parse_entry(entries[index], labware_labwhere_columns)

        entry_has_no_barcode = result_dict["unordered_barcode"] is None and result_dict["ordered_barcode"] is None
        entry_has_no_valid_user = result_dict["stored_by"] is None

        if entry_has_no_barcode or entry_has_no_valid_user:
            invalid_entries.append(result_dict)
        else:
            mlwh_entries.append(make_mlwh_entry(cast(LabwareLabwhereEntry, result_dict)))

    return mlwh_entries, invalid_entries


# sequencing_publisher
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


def make_sample_sequence_message_dicts(entries: Sequence[Any]) -> Sequence[SampleSequenceMessage]:
    """Parse entries into sample sequence messages.

    Arguments:
        entries {Sequence[Any]}: entries to parse

    Returns:
        sample_sequence_message_dicts {Sequence[SampleSequenceMessage]}: messages to publish to RabbitMQ
    """
    sample_sequence_message_dicts = []

    for index in range(len(entries)):
        message_dict = parse_entry(entries[index], run_status_columns)

        sample_sequence_message_dicts.append(cast(SampleSequenceMessage, message_dict))

    return sample_sequence_message_dicts
