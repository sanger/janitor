CREATE TABLE seq_product_irods_locations
(
    id_product varchar(255) NOT NULL,
    irods_root_collection varchar(255) NOT NULL,
    irods_data_relative_path varchar(255),
    irods_secondary_data_relative_path varchar(255)
);
