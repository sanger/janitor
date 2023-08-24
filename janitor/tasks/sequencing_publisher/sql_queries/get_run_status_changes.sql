SELECT
    run_status.date AS change_date,
    run_status.id_run AS id_run,
    study.name AS sequencing_study,
    sample.supplier_name AS sample_supplier_id,
    labware_subject.friendly_name AS labware_barcode,
    run_status.id_run_status AS run_status_id,
    irods.irods_root_collection AS irods_root_collection,
    -- note there can be multiple irods files per sequencing run per sample - we'll group these together to avoid multiple rows per irods file
    GROUP_CONCAT(irods.irods_data_relative_path ORDER BY irods.irods_data_relative_path SEPARATOR ';' ) AS irods_data_relative_paths,
    GROUP_CONCAT(irods.irods_secondary_data_relative_path ORDER BY irods.irods_secondary_data_relative_path SEPARATOR ';')  AS irods_secondary_data_relative_paths

FROM iseq_flowcell AS flowcell

-- join to sequencing tables, sequencing study and sample table
JOIN (
    iseq_product_metrics AS product_metrics,
    sample,
    study,
    iseq_run_status AS run_status
)

ON (
    product_metrics.id_iseq_flowcell_tmp = flowcell.id_iseq_flowcell_tmp
    AND sample.id_sample_tmp = flowcell.id_sample_tmp
    AND flowcell.id_study_tmp = study.id_study_tmp
    AND run_status.id_run = product_metrics.id_run
)

-- join to irods_location, left join in case it doesn't exist
LEFT JOIN seq_product_irods_locations irods ON irods.id_product=product_metrics.id_iseq_product

-- join to stock plate received into SeqOps, using left join in case it doesn't exist
LEFT JOIN (
-- sub query extract only the latest event which belongs to a sample manifest update for a given sample
    SELECT
        sample_subject.uuid AS sample_uuid,
        MAX(e2.id) AS manifest_update_event_id
    FROM mlwh_events.event_types et2
    JOIN mlwh_events.events e2 ON (e2.event_type_id=et2.id)

    -- JOIN ON sample subject/roles
    JOIN mlwh_events.roles sample_role ON (sample_role.event_id=e2.id)
    JOIN mlwh_events.role_types sample_role_rt ON (sample_role.role_type_id=sample_role_rt.id)
    JOIN mlwh_events.subjects sample_subject ON (sample_role.subject_id=sample_subject.id)

    WHERE
        e2.occured_at > %(latest_timestamp)s -- prevent querying data too old to be relevant
        AND et2.key='sample_manifest.updated'
        AND sample_role_rt.key='sample'
    GROUP BY sample_subject.uuid
) AS last_sample_manifest_updated_event
ON UNHEX(replace(sample.uuid_sample_lims, '-', ''))=last_sample_manifest_updated_event.sample_uuid

-- join to last manifest update event
JOIN mlwh_events.events e ON (e.id=last_sample_manifest_updated_event.manifest_update_event_id)

-- JOIN ON labware subject on manifest update event
JOIN mlwh_events.roles labware_role ON (labware_role.event_id=last_sample_manifest_updated_event.manifest_update_event_id)
JOIN mlwh_events.role_types labware_role_rt ON (labware_role.role_type_id=labware_role_rt.id)
JOIN mlwh_events.subjects labware_subject ON (labware_role.subject_id=labware_subject.id)

WHERE
    e.occured_at > %(latest_timestamp)s -- prevent querying data too old to be relevant
    AND labware_role_rt.key='labware' -- limit joins to event subject data to labware
    AND study.id_study_lims = '7454'  -- study id for SGE Mave samples
GROUP BY
    sample.supplier_name,run_status.id_run,
    change_date,
    labware_barcode,
    run_status_id,
    irods.irods_root_collection
ORDER BY
    sample.supplier_name,
    run_status.id_run,
    run_status.date;
