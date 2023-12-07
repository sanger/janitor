from datetime import datetime
from typing import Optional, TypedDict


# Databases
class DbConnectionDetails(TypedDict):
    host: str
    port: int
    db_name: str
    username: str
    password: str


# RabbitMQ
class RabbitMQDetails(TypedDict):
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    VHOST: str


# labware_location
class LabwareLabwhereEntry(TypedDict):
    labware_barcode: str
    unordered_barcode: Optional[str]
    unordered_full: Optional[str]
    unordered_name: Optional[str]
    ordered_barcode: Optional[str]
    ordered_full: Optional[str]
    ordered_name: Optional[str]
    coordinate_position: Optional[int]
    coordinate_row: Optional[int]
    coordinate_column: Optional[int]
    stored_by: str
    stored_at: str


class LabwareMLWHEntry(TypedDict):
    labware_barcode: str
    location_barcode: Optional[str]
    full_location_address: Optional[str]
    location_name: Optional[str]
    coordinate_position: Optional[int]
    coordinate_row: Optional[int]
    coordinate_column: Optional[int]
    lims_id: str
    stored_by: str
    stored_at: str
    created_at: str
    updated_at: str


# sequencing_publisher
class SampleSequenceMessage(TypedDict):
    change_date: datetime
    id_run: int
    sequencing_study: str
    sample_supplier_id: str
    labware_barcode: str
    run_status: int
    irods_root_collection: str
    irods_data_relative_path: Optional[str]
    irods_secondary_data_relative_path: Optional[str]
    latest_timestamp: datetime
