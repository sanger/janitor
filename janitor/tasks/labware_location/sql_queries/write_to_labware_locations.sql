INSERT INTO labware_location (
    labware_barcode,
    location_barcode,
    full_location_address,
    location_name,
    coordinate_position,
    coordinate_row,
    coordinate_column,
    lims_id,
    stored_by,
    stored_at,
    created_at,
    updated_at
)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    location_barcode = VALUES(location_barcode),
    full_location_address = VALUES(full_location_address),
    location_name = VALUES(location_name),
    coordinate_position = VALUES(coordinate_position),
    coordinate_row = VALUES(coordinate_row),
    coordinate_column = VALUES(coordinate_column),
    lims_id = VALUES(lims_id),
    stored_by = VALUES(stored_by),
    stored_at = VALUES(stored_at),
    updated_at = VALUES(updated_at);
