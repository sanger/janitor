CREATE TABLE audits (id int(11) primary key, auditable_id int(11), auditable_type varchar(255), user_id int(11), updated_at datetime(6));
