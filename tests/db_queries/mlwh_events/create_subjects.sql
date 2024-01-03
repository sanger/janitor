CREATE TABLE subjects
(
    id int(11) primary key NOT NULL AUTO_INCREMENT,
    uuid varchar(255) NOT NULL UNIQUE,
    friendly_name varchar(255) NOT NULL
);
