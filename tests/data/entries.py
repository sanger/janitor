from datetime import datetime, timedelta
from typing import Any, Dict

from tests.types import (
    AuditsTableEntry,
    CoordinatesTableEntry,
    LabwareLocationTableEntry,
    LabwaresTableEntry,
    LocationsTableEntry,
    UsersTableEntry,
)


def get_time(delta_mins: int) -> datetime:
    """
    Get current time minus specified number of minutes.

    Parameters:
        delta_mins {int}: Number of minutes to subtract

    Returns:
        {datetime}: Current time minus minutes
    """
    return (datetime.utcnow() - timedelta(minutes=delta_mins)).replace(microsecond=0)


class Entries:
    @property
    def good_input_entry_with_location_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=1, barcode="labware1", location_id=1, coordinate_id=None)],
            "audits": [
                AuditsTableEntry(
                    id=1,
                    auditable_id=1,
                    auditable_type="Labware",
                    user_id=1,
                    updated_at=get_time(delta_mins=3),
                )
            ],
            "users": [UsersTableEntry(id=1, login="user1")],
            "locations": [
                LocationsTableEntry(
                    id=1,
                    barcode="unordered_location1",
                    parentage="PARENT / unordered_location1",
                    name="unordered_location1",
                )
            ],
        }

    @property
    def good_input_entry_with_location_output(self) -> Dict[str, Any]:
        return {
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware1",
                    location_barcode="unordered_location1",
                    full_location_address="PARENT / unordered_location1",
                    location_name="unordered_location1",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user1",
                    stored_at=get_time(delta_mins=3),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                )
            ]
        }

    @property
    def good_input_entry_with_coordinates_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=2, barcode="labware2", location_id=None, coordinate_id=2)],
            "audits": [
                AuditsTableEntry(
                    id=2,
                    auditable_id=2,
                    auditable_type="Labware",
                    user_id=2,
                    updated_at=get_time(delta_mins=3),
                )
            ],
            "users": [UsersTableEntry(id=2, login="user2")],
            "locations": [
                LocationsTableEntry(
                    id=2, barcode="ordered_location2", parentage="PARENT / ordered_location2", name="ordered_location2"
                )
            ],
            "coordinates": [CoordinatesTableEntry(id=2, position=1, row=1, column=1, location_id=2)],
        }

    @property
    def good_input_entry_with_coordinates_output(self) -> Dict[str, Any]:
        return {
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware2",
                    location_barcode="ordered_location2",
                    full_location_address="PARENT / ordered_location2",
                    location_name="ordered_location2",
                    coordinate_position=1,
                    coordinate_row=1,
                    coordinate_column=1,
                    lims_id="LabWhere",
                    stored_by="user2",
                    stored_at=get_time(delta_mins=3),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                )
            ]
        }

    @property
    def good_input_entry_with_two_audits_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=3, barcode="labware3", location_id=3, coordinate_id=None)],
            "audits": [
                AuditsTableEntry(
                    id=3,
                    auditable_id=3,
                    auditable_type="Labware",
                    user_id=3,
                    updated_at=get_time(delta_mins=4),
                ),
                AuditsTableEntry(
                    id=4,
                    auditable_id=3,
                    auditable_type="Labware",
                    user_id=4,
                    updated_at=get_time(delta_mins=2),
                ),
            ],
            "users": [UsersTableEntry(id=3, login="user3"), UsersTableEntry(id=4, login="user4")],
            "locations": [
                LocationsTableEntry(
                    id=3,
                    barcode="unordered_location3",
                    parentage="PARENT / unordered_location3",
                    name="unordered_location3",
                )
            ],
        }

    @property
    def good_input_entry_with_two_audits_output(self) -> Dict[str, Any]:
        return {
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware3",
                    location_barcode="unordered_location3",
                    full_location_address="PARENT / unordered_location3",
                    location_name="unordered_location3",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user4",
                    stored_at=get_time(delta_mins=2),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                )
            ]
        }

    @property
    def good_input_entry_outdated_record_in_mlwh_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=4, barcode="labware4", location_id=4, coordinate_id=None)],
            "audits": [
                AuditsTableEntry(
                    id=1,
                    auditable_id=4,
                    auditable_type="Labware",
                    user_id=3,
                    updated_at=get_time(delta_mins=4),
                ),
                AuditsTableEntry(
                    id=2,
                    auditable_id=4,
                    auditable_type="Labware",
                    user_id=4,
                    updated_at=get_time(delta_mins=2),
                ),
            ],
            "users": [UsersTableEntry(id=3, login="user3"), UsersTableEntry(id=4, login="user4")],
            "locations": [
                LocationsTableEntry(
                    id=3,
                    barcode="unordered_location3",
                    parentage="PARENT / unordered_location3",
                    name="unordered_location3",
                ),
                LocationsTableEntry(
                    id=4,
                    barcode="unordered_location4",
                    parentage="PARENT / unordered_location4",
                    name="unordered_location4",
                ),
            ],
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware4",
                    location_barcode="unordered_location3",
                    full_location_address="PARENT / unordered_location3",
                    location_name="unordered_location3",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user3",
                    stored_at=get_time(delta_mins=4),
                    created_at=get_time(delta_mins=4),
                    updated_at=get_time(delta_mins=4),
                )
            ],
        }

    @property
    def good_input_entry_outdated_record_in_mlwh_output(self) -> Dict[str, Any]:
        return {
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware4",
                    location_barcode="unordered_location4",
                    full_location_address="PARENT / unordered_location4",
                    location_name="unordered_location4",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user4",
                    stored_at=get_time(delta_mins=2),
                    created_at=get_time(delta_mins=4),
                    updated_at=get_time(delta_mins=0),
                )
            ]
        }

    @property
    def bad_input_entry_without_location_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=5, barcode="labware5", location_id=None, coordinate_id=None)],
            "audits": [
                AuditsTableEntry(
                    id=5,
                    auditable_id=5,
                    auditable_type="Labware",
                    user_id=5,
                    updated_at=get_time(delta_mins=0),
                )
            ],
            "users": [UsersTableEntry(id=5, login="user5")],
        }

    @property
    def bad_input_entry_without_audits_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=6, barcode="labware6", location_id=6, coordinate_id=None)],
            "locations": [
                LocationsTableEntry(id=6, barcode="unordered_location6", parentage="PARENT / unordered_location6")
            ],
        }

    @property
    def bad_input_entry_without_location_without_audits_input(self) -> Dict[str, Any]:
        return {
            "labwares": [LabwaresTableEntry(id=7, barcode="labware7", location_id=None, coordinate_id=None)],
        }

    @property
    def mixed_entries_input(self) -> Dict[str, Any]:
        return {
            "labwares": [
                LabwaresTableEntry(id=1, barcode="labware1", location_id=1, coordinate_id=None),
                LabwaresTableEntry(id=2, barcode="labware2", location_id=None, coordinate_id=None),
                LabwaresTableEntry(id=3, barcode="labware3", location_id=None, coordinate_id=2),
                LabwaresTableEntry(id=4, barcode="labware4", location_id=3, coordinate_id=None),
                LabwaresTableEntry(id=5, barcode="labware5", location_id=3, coordinate_id=None),
                LabwaresTableEntry(id=6, barcode="labware6", location_id=None, coordinate_id=None),
                LabwaresTableEntry(id=7, barcode="labware7", location_id=4, coordinate_id=None),
            ],
            "audits": [
                AuditsTableEntry(
                    id=1,
                    auditable_id=1,
                    auditable_type="Labware",
                    user_id=1,
                    updated_at=get_time(delta_mins=4),
                ),
                AuditsTableEntry(
                    id=2,
                    auditable_id=2,
                    auditable_type="Labware",
                    user_id=2,
                    updated_at=get_time(delta_mins=4),
                ),
                AuditsTableEntry(
                    id=3,
                    auditable_id=3,
                    auditable_type="Labware",
                    user_id=3,
                    updated_at=get_time(delta_mins=3),
                ),
                AuditsTableEntry(
                    id=4,
                    auditable_id=5,
                    auditable_type="Labware",
                    user_id=5,
                    updated_at=get_time(delta_mins=2),
                ),
                AuditsTableEntry(
                    id=5,
                    auditable_id=7,
                    auditable_type="Labware",
                    user_id=7,
                    updated_at=get_time(delta_mins=1),
                ),
            ],
            "users": [
                UsersTableEntry(id=1, login="user1"),
                UsersTableEntry(id=2, login="user2"),
                UsersTableEntry(id=3, login="user3"),
                UsersTableEntry(id=4, login="user4"),
                UsersTableEntry(id=5, login="user5"),
                UsersTableEntry(id=6, login="user6"),
                UsersTableEntry(id=7, login="user7"),
            ],
            "locations": [
                LocationsTableEntry(
                    id=1,
                    barcode="unordered_location1",
                    parentage="PARENT / unordered_location1",
                    name="unordered_location1",
                ),
                LocationsTableEntry(
                    id=2, barcode="ordered_location2", parentage="PARENT / ordered_location2", name="ordered_location2"
                ),
                LocationsTableEntry(
                    id=3,
                    barcode="unordered_location3",
                    parentage="PARENT / unordered_location3",
                    name="unordered_location3",
                ),
                LocationsTableEntry(
                    id=4,
                    barcode="unordered_location4",
                    parentage="PARENT / unordered_location4",
                    name="unordered_location4",
                ),
            ],
            "coordinates": [CoordinatesTableEntry(id=2, position=1, row=1, column=1, location_id=2)],
        }

    @property
    def mixed_entries_output(self) -> Dict[str, Any]:
        return {
            "labware_location": [
                LabwareLocationTableEntry(
                    id=1,
                    labware_barcode="labware1",
                    location_barcode="unordered_location1",
                    full_location_address="PARENT / unordered_location1",
                    location_name="unordered_location1",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user1",
                    stored_at=get_time(delta_mins=4),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                ),
                LabwareLocationTableEntry(
                    id=2,
                    labware_barcode="labware3",
                    location_barcode="ordered_location2",
                    full_location_address="PARENT / ordered_location2",
                    location_name="ordered_location2",
                    coordinate_position=1,
                    coordinate_row=1,
                    coordinate_column=1,
                    lims_id="LabWhere",
                    stored_by="user3",
                    stored_at=get_time(delta_mins=3),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                ),
                LabwareLocationTableEntry(
                    id=3,
                    labware_barcode="labware5",
                    location_barcode="unordered_location3",
                    full_location_address="PARENT / unordered_location3",
                    location_name="unordered_location3",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user5",
                    stored_at=get_time(delta_mins=2),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                ),
                LabwareLocationTableEntry(
                    id=4,
                    labware_barcode="labware7",
                    location_barcode="unordered_location4",
                    full_location_address="PARENT / unordered_location4",
                    location_name="unordered_location4",
                    coordinate_position=None,
                    coordinate_row=None,
                    coordinate_column=None,
                    lims_id="LabWhere",
                    stored_by="user7",
                    stored_at=get_time(delta_mins=1),
                    created_at=get_time(delta_mins=0),
                    updated_at=get_time(delta_mins=0),
                ),
            ]
        }
