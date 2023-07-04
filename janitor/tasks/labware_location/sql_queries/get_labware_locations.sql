SELECT
	lw.id,
	lw.barcode AS labware_barcode,
	loc1.barcode AS unordered_barcode,
	loc1.parentage AS unordered_full,
	loc2.barcode AS ordered_barcode,
	loc2.parentage AS ordered_full,
	coords.position AS coordinate_position,
	coords.row AS coordinate_row,
	coords.column AS coordinate_column,
	users.login AS stored_by,
	audits.updated_at AS stored_at
FROM
	labwares lw
LEFT JOIN locations loc1 ON
	lw.location_id = loc1.id
LEFT JOIN coordinates coords ON
	lw.coordinate_id = coords.id
LEFT JOIN locations loc2 ON
	coords.location_id = loc2.id
LEFT JOIN audits ON
	lw.id = audits.auditable_id
	AND audits.auditable_type = "Labware"
LEFT JOIN users ON
	audits.user_id = users.id
LEFT JOIN audits audits_b ON
	audits.auditable_id = audits_b.auditable_id
	AND audits_b.auditable_type = "Labware"
	AND audits.id < audits_b.id
WHERE
	audits_b.updated_at IS NULL
	AND audits.updated_at >= %(latest_timestamp)s;
