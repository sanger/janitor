from datetime import datetime
from typing import Any, Dict

from tests.types import (
    EventsTableEntry,
    EventTypesTableEntry,
    IseqFlowcellTableEntry,
    IseqProductMetricsTableEntry,
    IseqRunStatusTableEntry,
    RolesTableEntry,
    RoleTypesTableEntry,
    SampleTableEntry,
    SeqProductsIrodsLocationsTableEntry,
    StudyTableEntry,
    SubjectsTableEntry,
)


class Entries:
    @property
    def good_input_entry(self) -> Dict[str, Any]:
        return {
            "events": [
                EventsTableEntry(id=4318860, event_type_id=413, occured_at=datetime(2023, 9, 11, 9, 10, 43)),
            ],
            "event_types": [
                EventTypesTableEntry(id=413, key="sample_manifest.updated"),
            ],
            "roles": [
                RolesTableEntry(event_id=4318860, role_type_id=9, subject_id=8788481),
                RolesTableEntry(event_id=4318860, role_type_id=6, subject_id=8826191),
            ],
            "role_types": [
                RoleTypesTableEntry(id=6, key="sample"),
                RoleTypesTableEntry(id=9, key="labware"),
            ],
            "subjects": [
                SubjectsTableEntry(id=8788481, uuid="uuid", friendly_name="labware_barcode"),
                SubjectsTableEntry(id=8826191, uuid="sample_uuid", friendly_name="labware_barcode"),
            ],
            "iseq_flowcell": [
                IseqFlowcellTableEntry(id_iseq_flowcell_tmp=12247786, id_sample_tmp=8961016, id_study_tmp=5653),
            ],
            "iseq_product_metrics": [
                IseqProductMetricsTableEntry(
                    id_iseq_product="id_product",
                    id_iseq_flowcell_tmp=12247786,
                    id_run=47819,
                ),
            ],
            "iseq_run_status": [
                IseqRunStatusTableEntry(id_run=47819, date=datetime(2023, 9, 11, 9, 10, 43), id_run_status_dict=1),
            ],
            "sample": [
                SampleTableEntry(
                    id_sample_tmp=8961016,
                    uuid_sample_lims="sample_uuid",
                    supplier_name="sample_supplier_id",
                ),
            ],
            "seq_product_irods_locations": [
                SeqProductsIrodsLocationsTableEntry(
                    id_product="id_product",
                    irods_root_collection="root_collection",
                    irods_data_relative_path="data_relative",
                    irods_secondary_data_relative_path=None,
                ),
            ],
            "study": [
                StudyTableEntry(
                    id_study_tmp=5653,
                    name="sequencing_study",
                ),
            ],
        }
