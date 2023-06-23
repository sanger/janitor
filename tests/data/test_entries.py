from datetime import datetime
from tests.types import (
    LabwaresTableEntry,
    AuditsTableEntry,
    UsersTableEntry,
    LocationsTableEntry,
    CoordinatesTableEntry,
    LabwareLocationTableEntry,
)


TEST_ENTRIES = {
    "good_input_entry_with_location": {
        "labwares": [LabwaresTableEntry(id=1, barcode="labware1", location_id=1, coordinate_id=None)],
        "audits": [
            AuditsTableEntry(id=1, auditable_id=1, auditable_type="Labware", user_id=1, updated_at=datetime.utcnow())
        ],
        "users": [UsersTableEntry(id=1, login="user1")],
        "locations": [
            LocationsTableEntry(id=1, barcode="unordered_location1", parentage="PARENT / unordered_location1")
        ],
    },
    "good_input_entry_with_coordinates": {
        "labwares": [LabwaresTableEntry(id=2, barcode="labware2", location_id=None, coordinate_id=2)],
        "audits": [
            AuditsTableEntry(id=2, auditable_id=2, auditable_type="Labware", user_id=2, updated_at=datetime.utcnow())
        ],
        "users": [UsersTableEntry(id=2, login="user2")],
        "locations": [LocationsTableEntry(id=2, barcode="ordered_location2", parentage="PARENT / ordered_location2")],
        "coordinates": [CoordinatesTableEntry(id=2, position=1, row=1, column=1, location_id=2)],
    },
    "good_input_entry_with_two_audits": {
        "labwares": [LabwaresTableEntry(id=3, barcode="labware3", location_id=3, coordinate_id=None)],
        "audits": [
            AuditsTableEntry(id=3, auditable_id=3, auditable_type="Labware", user_id=3, updated_at=datetime.utcnow()),
            AuditsTableEntry(id=4, auditable_id=3, auditable_type="Labware", user_id=4, updated_at=datetime.utcnow()),
        ],
        "users": [UsersTableEntry(id=3, login="user3"), UsersTableEntry(id=4, login="user4")],
        "locations": [
            LocationsTableEntry(id=3, barcode="unordered_location3", parentage="PARENT / unordered_location3")
        ],
    },
    "bad_input_entry_without_location_info": {
        "labwares": [LabwaresTableEntry(id=4, barcode="labware4", location_id=None, coordinate_id=None)],
        "audits": [
            AuditsTableEntry(id=5, auditable_id=4, auditable_type="Labware", user_id=5, updated_at=datetime.utcnow())
        ],
        "users": [UsersTableEntry(id=5, login="user5")],
    },
    "bad_input_entry_with_location_without_audits": {
        "labwares": [LabwaresTableEntry(id=5, barcode="labware5", location_id=4, coordinate_id=None)],
        "locations": [
            LocationsTableEntry(id=4, barcode="unordered_location4", parentage="PARENT / unordered_location4")
        ],
    },
    "bad_input_entry_with_coordinates_without_audits": {
        "labwares": [LabwaresTableEntry(id=6, barcode="labware6", location_id=None, coordinate_id=5)],
        "locations": [LocationsTableEntry(id=5, barcode="ordered_location5", parentage="PARENT / ordered_location5")],
        "coordinates": [CoordinatesTableEntry(id=5, position=1, row=1, column=1, location_id=5)],
    },
    "bad_input_entry_without_location_without_audits": {
        "labwares": [LabwaresTableEntry(id=7, barcode="labware7", location_id=None, coordinate_id=None)],
    },
    "good_updated_input_entry": {
        "labwares": [LabwaresTableEntry(id=1, barcode="labware1", location_id=3, coordinate_id=None)],
        "audits": [
            AuditsTableEntry(id=1, auditable_id=1, auditable_type="Labware", user_id=1, updated_at=datetime.utcnow()),
            AuditsTableEntry(id=2, auditable_id=1, auditable_type="Labware", user_id=3, updated_at=datetime.utcnow()),
        ],
        "users": [UsersTableEntry(id=1, login="user1"), UsersTableEntry(id=3, login="user3")],
        "locations": [
            LocationsTableEntry(id=1, barcode="unordered_location1", parentage="PARENT / unordered_location1"),
            LocationsTableEntry(id=3, barcode="unordered_location3", parentage="PARENT / unordered_location3"),
        ],
        "coordinates": [CoordinatesTableEntry(id=2, position=1, row=1, column=1, location_id=2)],
    },
    "good_outdated_output_entry": {
        "labware_location": [
            LabwareLocationTableEntry(
                id=1,
                labware_barcode="labware1",
                location_barcode="unordered_location1",
                full_location_address="PARENT / unordered_location1",
                coordinate_position=None,
                coordinate_row=None,
                coordinate_column=None,
                lims_id="LabWhere",
                stored_by="user1",
                stored_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        ]
    },
}
