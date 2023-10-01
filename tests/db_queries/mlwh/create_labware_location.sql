CREATE TABLE labware_location
(
    id int(11) primary key NOT NULL AUTO_INCREMENT,
    labware_barcode varchar(255) NOT NULL UNIQUE,
    location_barcode varchar(255) NOT NULL,
    full_location_address varchar(255) NOT NULL,
    coordinate_position int(11),
    coordinate_row int(11),
    coordinate_column int(11),
    lims_id varchar(255) NOT NULL,
    stored_by varchar(255) NOT NULL,
    stored_at datetime(6) NOT NULL,
    created_at datetime(6) NOT NULL,
    updated_at datetime(6) NOT NULL
);
