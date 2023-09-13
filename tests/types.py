from datetime import datetime
from typing import Optional, TypedDict


# labware_location
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


# sequencing_publisher
class EventsTableEntry(TypedDict):
    id: int
    event_type_id: int
    occured_at: datetime


class EventTypesTableEntry(TypedDict):
    id: int
    key: str


class IseqFlowcellTableEntry(TypedDict):
    id_iseq_flowcell_tmp: int
    id_sample_tmp: int
    id_study_tmp: Optional[int]


class IseqProductMetricsTableEntry(TypedDict):
    id_iseq_product: str
    id_iseq_flowcell_tmp: Optional[int]
    id_run: Optional[int]


class IseqRunStatusTableEntry(TypedDict):
    id_run: int
    date: datetime
    id_run_status_dict: int


class RolesTableEntry(TypedDict):
    event_id: int
    subject_id: int
    role_type_id: int


class RoleTypesTableEntry(TypedDict):
    id: int
    key: str


class SampleTableEntry(TypedDict):
    id_sample_tmp: int
    uuid_sample_lims: Optional[str]
    supplier_name: Optional[str]


class SeqProductsIrodsLocationsTableEntry(TypedDict):
    id_product: str
    irods_root_collection: str
    irods_data_relative_path: Optional[str]
    irods_secondary_data_relative_path: Optional[str]


class StudyTableEntry(TypedDict):
    id_study_tmp: int
    name: Optional[str]


class SubjectsTableEntry(TypedDict):
    id: int
    uuid: str
    friendly_name: str
