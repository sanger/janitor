import logging.config
from copy import deepcopy

import pytest

from janitor.db.database import Database
from janitor.helpers.config_helpers import get_config
from janitor.types import DbConnectionDetails

CONFIG = get_config("janitor.config.test")
logging.config.dictConfig(CONFIG.LOGGING)


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
