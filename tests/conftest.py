import logging.config
from copy import deepcopy
from unittest.mock import patch

import pytest

from janitor.db.database import Database
from janitor.helpers.config_helpers import get_config
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


def clear_lw_tables(lw_database):
    # Labwares table
    drop_table_query = "DROP TABLE IF EXISTS labwares;"
    lw_database.execute_query(drop_table_query, {})

    labwares_cols = "id int(11) primary key, barcode varchar(255), location_id int(11), coordinate_id int(11)"
    create_table_query = f"CREATE TABLE labwares ({labwares_cols});"
    lw_database.execute_query(create_table_query, {})

    # Audits table
    drop_table_query = "DROP TABLE IF EXISTS audits;"
    lw_database.execute_query(drop_table_query, {})

    audits_cols = """
    id int(11) primary key, auditable_id int(11), auditable_type varchar(255), user_id int(11), updated_at datetime(6)
    """
    create_table_query = f"CREATE TABLE audits ({audits_cols});"
    lw_database.execute_query(create_table_query, {})

    # Users table
    drop_table_query = "DROP TABLE IF EXISTS users;"
    lw_database.execute_query(drop_table_query, {})

    users_cols = "id int(11) primary key, login varchar(255)"
    create_table_query = f"CREATE TABLE users ({users_cols});"
    lw_database.execute_query(create_table_query, {})

    # Locations table
    drop_table_query = "DROP TABLE IF EXISTS locations;"
    lw_database.execute_query(drop_table_query, {})

    locations_cols = "id int(11) primary key, barcode varchar(255), parentage varchar(255)"
    create_table_query = f"CREATE TABLE locations ({locations_cols});"
    lw_database.execute_query(create_table_query, {})

    # Coordinates table
    drop_table_query = "DROP TABLE IF EXISTS coordinates;"
    lw_database.execute_query(drop_table_query, {})

    coordinates_cols = (
        "id int(11) primary key, `position` int(11), `row` int(11), `column` int(11), location_id int(11)"
    )
    create_table_query = f"CREATE TABLE coordinates ({coordinates_cols});"
    lw_database.execute_query(create_table_query, {})


def clear_mlwh_tables(mlwh_database):
    # Labware location table
    drop_table_query = "DROP TABLE IF EXISTS labware_location;"
    mlwh_database.execute_query(drop_table_query, {})

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
    create_table_query = f"CREATE TABLE labware_location ({labware_location_cols});"
    mlwh_database.execute_query(create_table_query, {})
