CREATE TABLE iseq_product_metrics
(
    id_iseq_product varchar(255) NOT NULL UNIQUE,
    id_iseq_flowcell_tmp int(11),
    id_run int(11)
);
