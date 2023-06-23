import pytest
import logging.config
from copy import deepcopy
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


@pytest.fixture(params=[[]])
def lw_labwares_table(lw_database, request):
    table_name = "labwares"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    lw_database.execute_query(drop_table_query, {})

    cols = "id int(11) primary key, barcode varchar(255), location_id int(11), coordinate_id int(11)"
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    lw_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = (
            f"INSERT INTO {table_name} (id, barcode, location_id, coordinate_id) VALUES (%s, %s, %s, %s);"
        )
        lw_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))


@pytest.fixture(params=[[]])
def lw_audits_table(lw_database, request):
    table_name = "audits"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    lw_database.execute_query(drop_table_query, {})

    cols = "id int(11) primary key, auditable_id int(11), auditable_type varchar(255), user_id int(11), updated_at datetime(6)"
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    lw_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = f"INSERT INTO {table_name} (id, auditable_id, auditable_type, user_id, updated_at) VALUES (%s, %s, %s, %s, %s);"
        lw_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))


@pytest.fixture(params=[[]])
def lw_users_table(lw_database, request):
    table_name = "users"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    lw_database.execute_query(drop_table_query, {})

    cols = "id int(11) primary key, login varchar(255)"
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    lw_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = f"INSERT INTO {table_name} (id, login) VALUES (%s, %s);"
        lw_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))


@pytest.fixture(params=[[]])
def lw_locations_table(lw_database, request):
    table_name = "locations"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    lw_database.execute_query(drop_table_query, {})

    cols = "id int(11) primary key, barcode varchar(255), parentage varchar(255)"
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    lw_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = f"INSERT INTO {table_name} (id, barcode, parentage) VALUES (%s, %s, %s);"
        lw_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))


@pytest.fixture(params=[[]])
def lw_coordinates_table(lw_database, request):
    table_name = "coordinates"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    lw_database.execute_query(drop_table_query, {})

    cols = "id int(11) primary key, `position` int(11), `row` int(11), `column` int(11), location_id int(11)"
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    lw_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = (
            f"INSERT INTO {table_name} (id, `position`, `row`, `column`, location_id) VALUES (%s, %s, %s, %s, %s);"
        )
        lw_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))


@pytest.fixture(params=[[]])
def mlwh_labware_locations_table(mlwh_database, request):
    table_name = "labware_location"
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    mlwh_database.execute_query(drop_table_query, {})

    cols = """
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
    create_table_query = f"CREATE TABLE {table_name} ({cols});"
    mlwh_database.execute_query(create_table_query, {})

    if request.param:
        insert_into_table_query = f"""
                INSERT INTO {table_name}
                (
                    id,
                    labware_barcode,
                    location_barcode,
                    full_location_address,
                    coordinate_position,
                    coordinate_row,
                    coordinate_column,
                    lims_id,
                    stored_by,
                    stored_at,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        mlwh_database.write_entries_to_table(insert_into_table_query, request.param, len(request.param))
