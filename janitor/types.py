from typing import Optional, TypedDict


class DbConnectionDetails(TypedDict):
    host: str
    port: int
    db_name: str
    username: str
    password: str


class LabwareLabwhereEntry(TypedDict):
    labware_barcode: str
    unordered_barcode: Optional[str]
    unordered_full: Optional[str]
    ordered_barcode: Optional[str]
    ordered_full: Optional[str]
    coordinate_position: Optional[int]
    coordinate_row: Optional[int]
    coordinate_column: Optional[int]
    stored_by: str
    stored_at: str


class LabwareMLWHEntry(TypedDict):
    labware_barcode: str
    location_barcode: Optional[str]
    full_location_address: Optional[str]
    coordinate_position: Optional[int]
    coordinate_row: Optional[int]
    coordinate_column: Optional[int]
    lims_id: str
    stored_by: str
    stored_at: str
    created_at: str
    updated_at: str
