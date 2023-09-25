import logging.config
from copy import deepcopy
from unittest.mock import PropertyMock, patch

import pytest

from janitor.db.database import Database
from janitor.helpers.config_helpers import get_config
from janitor.helpers.mysql_helpers import load_query
from janitor.rabbitmq.rabbit import Rabbit
from janitor.types import DbConnectionDetails

CONFIG = get_config("janitor.config.test")
logging.config.dictConfig(CONFIG.LOGGING)

from pathlib import Path

DB_QUERIES_FOLDERPATH = Path("tests/db_queries")


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


def recreate_all_tables(db, db_name, table_names):
    db.execute_query(load_query(DB_QUERIES_FOLDERPATH / db_name / "drop_tables.sql"), {})

    for table in table_names:
        db.execute_query(load_query(DB_QUERIES_FOLDERPATH / db_name / f"create_{table}.sql"), {})


def clear_lw_tables(lw_database):
    table_names = ["audits", "coordinates", "labwares", "locations", "users"]
    recreate_all_tables(lw_database, "lw", table_names)


def clear_mlwh_tables(mlwh_database):
    table_names = [
        "labware_location",
        "iseq_flowcell",
        "iseq_product_metrics",
        "iseq_run_status",
        "sample",
        "seq_product_irods_locations",
        "study",
    ]
    recreate_all_tables(mlwh_database, "mlwh", table_names)


def clear_mlwh_events_tables(mlwh_events_database):
    table_names = [
        "events",
        "event_types",
        "roles",
        "role_types",
        "subjects",
    ]
    recreate_all_tables(mlwh_events_database, "mlwh_events", table_names)
