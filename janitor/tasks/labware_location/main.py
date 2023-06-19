import logging
from os import path
from janitor.db.database import Database, DbConnectionDetails
from janitor.helpers.mysql_helpers import load_query
from janitor.helpers.mlwh_helpers import sort_results

wd = path.realpath(path.dirname(__file__))
logger = logging.getLogger(__name__)

get_locations_file = "get_labware_locations.sql"
add_to_labware_locations_file = "write_to_labware_locations.sql"

labwhere: DbConnectionDetails = {
    "host": "localhost",
    "port": 3000,
    "db_name": "labwhere_prod",
    "username": "root",
    "password": "",
}

mlwh: DbConnectionDetails = {
    "host": "localhost",
    "port": 3000,
    "db_name": "unified_warehouse_development",
    "username": "root",
    "password": "",
}


def sync_changes_from_labwhere():
    db_labwhere = Database(labwhere)
    db_mlwh = Database(mlwh)

    results = db_labwhere.execute_query(
        load_query(path.join(wd, "sql_queries", get_locations_file))
    )

    mlwh_entries, invalid_entries = sort_results(results)

    if invalid_entries:
        for entry in invalid_entries:
            logger.warning(f"Found invalid entry: {entry}")

    db_mlwh.write_entries_to_table(
        load_query(path.join(wd, "sql_queries", add_to_labware_locations_file)),
        mlwh_entries,
        5000,
    )

    db_labwhere.close()
    db_mlwh.close()
