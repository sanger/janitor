CREATE TABLE sample
(
    id_sample_tmp int(11) primary key NOT NULL AUTO_INCREMENT,
    uuid_sample_lims varchar(255) UNIQUE,
    supplier_name varchar(255)
);
