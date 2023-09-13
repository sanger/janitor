import logging.config
from copy import deepcopy
from unittest.mock import PropertyMock, patch

import pytest

from janitor.db.database import Database
from janitor.helpers.config_helpers import get_config
from janitor.rabbitmq.rabbit import Rabbit
from janitor.types import DbConnectionDetails

CONFIG = get_config("janitor.config.test")
logging.config.dictConfig(CONFIG.LOGGING)


@pytest.fixture
def mock_info():
    with patch("logging.info") as mock_logging_info:
        yield mock_logging_info


@pytest.fixture
def mock_error():
    with patch("logging.error") as mock_logging_error:
        yield mock_logging_error


@pytest.fixture
def config():
    return CONFIG


@pytest.fixture
def mlwh_database(mlwh_creds):
    try:
        # Create the database if it doesn't exist
        creds_without_database = deepcopy(mlwh_creds)
        creds_without_database["db_name"] = ""

        new_sql_conn = Database(creds_without_database)
        new_sql_conn.execute_query(f"CREATE DATABASE IF NOT EXISTS {mlwh_creds['db_name']}", {})
    finally:
        new_sql_conn.close()

    try:
        mysql_conn = Database(mlwh_creds)
        clear_mlwh_tables(mysql_conn)
        yield mysql_conn
    finally:
        mysql_conn.close()


@pytest.fixture
def mlwh_creds(config):
    return DbConnectionDetails(
        host=config.MLWH_DB["host"],
        db_name=config.MLWH_DB["db_name"],
        username=config.MLWH_DB["username"],
        password=config.MLWH_DB["password"],
        port=config.MLWH_DB["port"],
    )


@pytest.fixture
def mlwh_events_database(mlwh_events_creds):
    try:
        # Create the database if it doesn't exist
        creds_without_database = deepcopy(mlwh_events_creds)
        creds_without_database["db_name"] = ""

        new_sql_conn = Database(creds_without_database)
        new_sql_conn.execute_query(f"CREATE DATABASE IF NOT EXISTS {mlwh_events_creds['db_name']}", {})
    finally:
        new_sql_conn.close()

    try:
        mysql_conn = Database(mlwh_events_creds)
        clear_mlwh_events_tables(mysql_conn)
        yield mysql_conn
    finally:
        mysql_conn.close()


@pytest.fixture
def mlwh_events_creds(config):
    return config.MLWH_EVENTS_DB


@pytest.fixture
def lw_database(lw_creds):
    try:
        # Create the database if it doesn't exist
        creds_without_database = deepcopy(lw_creds)
        creds_without_database["db_name"] = ""

        new_sql_conn = Database(creds_without_database)
        new_sql_conn.execute_query(f"CREATE DATABASE IF NOT EXISTS {lw_creds['db_name']}", {})
    finally:
        new_sql_conn.close()

    try:
        mysql_conn = Database(lw_creds)
        clear_lw_tables(mysql_conn)
        yield mysql_conn
    finally:
        mysql_conn.close()


@pytest.fixture
def lw_creds(config):
    return DbConnectionDetails(
        host=config.LABWHERE_DB["host"],
        db_name=config.LABWHERE_DB["db_name"],
        username=config.LABWHERE_DB["username"],
        password=config.LABWHERE_DB["password"],
        port=config.LABWHERE_DB["port"],
    )


@pytest.fixture
def mock_rabbit(config):
    with patch("janitor.rabbitmq.rabbit.Rabbit.connection", new_callable=PropertyMock) as mock_connection:
        mock_rabbit = Rabbit(config)
        mock_rabbit._connection = mock_connection
        yield mock_rabbit


def drop_and_recreate_table(db, table_name, cols):
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    db.execute_query(drop_table_query, {})

    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    db.execute_query(create_table_query, {})


def clear_lw_tables(lw_database):
    # Labwares table
    labwares_table_name = "labwares"
    labwares_cols = "id int(11) primary key, barcode varchar(255), location_id int(11), coordinate_id int(11)"
    drop_and_recreate_table(db=lw_database, table_name=labwares_table_name, cols=labwares_cols)

    # Audits table
    audits_table_name = "audits"
    audits_cols = """
    id int(11) primary key, auditable_id int(11), auditable_type varchar(255), user_id int(11), updated_at datetime(6)
    """
    drop_and_recreate_table(db=lw_database, table_name=audits_table_name, cols=audits_cols)

    # Users table
    users_table_name = "users"
    users_cols = "id int(11) primary key, login varchar(255)"
    drop_and_recreate_table(db=lw_database, table_name=users_table_name, cols=users_cols)

    # Locations table
    locations_table_name = "locations"
    locations_cols = "id int(11) primary key, barcode varchar(255), parentage varchar(255)"
    drop_and_recreate_table(db=lw_database, table_name=locations_table_name, cols=locations_cols)

    # Coordinates table
    coordinates_table_name = "coordinates"
    coordinates_cols = (
        "id int(11) primary key, `position` int(11), `row` int(11), `column` int(11), location_id int(11)"
    )
    drop_and_recreate_table(db=lw_database, table_name=coordinates_table_name, cols=coordinates_cols)


def clear_mlwh_tables(mlwh_database):
    # Labware location table
    labware_location_table_name = "labware_location"
    labware_location_cols = """
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
    """
    drop_and_recreate_table(db=mlwh_database, table_name=labware_location_table_name, cols=labware_location_cols)

    # Iseq flowcell table
    iseq_flowcell_table_name = "iseq_flowcell"
    iseq_flowcell_cols = """
        id_iseq_flowcell_tmp int(11) primary key NOT NULL AUTO_INCREMENT,
        id_sample_tmp int(11) NOT NULL,
        id_study_tmp int(11)
    """
    drop_and_recreate_table(db=mlwh_database, table_name=iseq_flowcell_table_name, cols=iseq_flowcell_cols)

    # Iseq product metrics table
    iseq_product_metrics_table_name = "iseq_product_metrics"
    iseq_product_metrics_cols = """
        id_iseq_product varchar(255) NOT NULL UNIQUE,
        id_iseq_flowcell_tmp int(11),
        id_run int(11)
    """
    drop_and_recreate_table(
        db=mlwh_database, table_name=iseq_product_metrics_table_name, cols=iseq_product_metrics_cols
    )

    # Iseq run status table
    iseq_run_status_table_name = "iseq_run_status"
    iseq_run_status_cols = """
        id_run int(11) NOT NULL,
        date datetime NOT NULL,
        id_run_status_dict int(11) NOT NULL
    """
    drop_and_recreate_table(db=mlwh_database, table_name=iseq_run_status_table_name, cols=iseq_run_status_cols)

    # Sample table
    sample_table_name = "sample"
    sample_cols = """
        id_sample_tmp int(11) primary key NOT NULL AUTO_INCREMENT,
        uuid_sample_lims varchar(255) UNIQUE,
        supplier_name varchar(255)
    """
    drop_and_recreate_table(db=mlwh_database, table_name=sample_table_name, cols=sample_cols)

    # Seq products irods locations table
    seq_product_irods_locations_table_name = "seq_product_irods_locations"
    seq_product_irods_locations_cols = """
        id_product varchar(255) NOT NULL,
        irods_root_collection varchar(255) NOT NULL,
        irods_data_relative_path varchar(255),
        irods_secondary_data_relative_path varchar(255)
    """
    drop_and_recreate_table(
        db=mlwh_database, table_name=seq_product_irods_locations_table_name, cols=seq_product_irods_locations_cols
    )

    # Study table
    study_table_name = "study"
    study_cols = """
        id_study_tmp int(11) primary key NOT NULL AUTO_INCREMENT,
        name varchar(255)
    """
    drop_and_recreate_table(db=mlwh_database, table_name=study_table_name, cols=study_cols)


def clear_mlwh_events_tables(mlwh_events_database):
    # Events table
    events_table_name = "events"
    events_cols = """
        id int(11) primary key NOT NULL AUTO_INCREMENT,
        event_type_id int(11) NOT NULL,
        occured_at datetime NOT NULL
    """
    drop_and_recreate_table(db=mlwh_events_database, table_name=events_table_name, cols=events_cols)

    # Event types table
    event_types_table_name = "event_types"
    event_types_cols = """
        id int(11) primary key NOT NULL AUTO_INCREMENT,
        `key` varchar(255) NOT NULL UNIQUE
    """
    drop_and_recreate_table(db=mlwh_events_database, table_name=event_types_table_name, cols=event_types_cols)

    # Roles table
    roles_table_name = "roles"
    roles_cols = """
        event_id int(11) NOT NULL,
        role_type_id int(11) NOT NULL,
        subject_id int(11) NOT NULL
    """
    drop_and_recreate_table(db=mlwh_events_database, table_name=roles_table_name, cols=roles_cols)

    # Role types table
    role_types_table_name = "role_types"
    role_types_cols = """
        id int(11) NOT NULL,
        `key` varchar(255) NOT NULL UNIQUE
    """
    drop_and_recreate_table(db=mlwh_events_database, table_name=role_types_table_name, cols=role_types_cols)

    # Subjects table
    subjects_table_name = "subjects"
    subjects_cols = """
        id int(11) primary key NOT NULL AUTO_INCREMENT,
        uuid varchar(255) NOT NULL UNIQUE,
        friendly_name varchar(255) NOT NULL
    """
    drop_and_recreate_table(db=mlwh_events_database, table_name=subjects_table_name, cols=subjects_cols)
