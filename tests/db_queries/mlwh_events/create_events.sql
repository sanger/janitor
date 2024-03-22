CREATE TABLE events
(
    id int(11) primary key NOT NULL AUTO_INCREMENT,
    event_type_id int(11) NOT NULL,
    occured_at datetime NOT NULL
);
