SELECT
  lw.id,
  lw.barcode labware_barcode,
  loc1.barcode unordered_barcode,
  loc1.parentage unordered_full,
  loc1.name unordered_name,
  loc2.barcode ordered_barcode,
  loc2.parentage ordered_full,
  loc2.name ordered_name,
  coords.position coordinate_position,
  coords.row coordinate_row,
  coords.column coordinate_column,
  users.login stored_by,
  audits.updated_at stored_at
FROM labwares lw
LEFT JOIN locations loc1 ON lw.location_id = loc1.id
LEFT JOIN coordinates coords ON lw.coordinate_id = coords.id
LEFT JOIN locations loc2 ON coords.location_id = loc2.id
LEFT JOIN audits
  ON lw.id = audits.auditable_id
  AND audits.auditable_type = "Labware"
LEFT JOIN users ON audits.user_id = users.id
LEFT JOIN audits audits_b
  ON audits.auditable_id = audits_b.auditable_id
  AND audits_b.auditable_type = "Labware"
  AND audits.id < audits_b.id

WHERE audits_b.updated_at IS NULL
AND audits.updated_at >= %(latest_timestamp)s

ORDER BY stored_at ASC;
