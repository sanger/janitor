from typing import TypedDict, Optional
from datetime import datetime


class LabwaresTableEntry(TypedDict):
    id: int
    barcode: str
    location_id: Optional[int]
    coordinate_id: Optional[int]


class AuditsTableEntry(TypedDict):
    id: int
    auditable_id: int
    auditable_type: str
    user_id: int
    updated_at: datetime


class UsersTableEntry(TypedDict):
    id: int
    login: str


class LocationsTableEntry(TypedDict):
    id: int
    barcode: str
    parentage: str


class CoordinatesTableEntry(TypedDict):
    id: int
    position: int
    row: int
    column: int
    location_id: int


class LabwareLocationTableEntry(TypedDict):
    id: int
    labware_barcode: str
    location_barcode: str
    full_location_address: str
    coordinate_position: Optional[int]
    coordinate_row: Optional[int]
    coordinate_column: Optional[int]
    lims_id: str
    stored_by: str
    stored_at: datetime
    created_at: datetime
    updated_at: datetime
