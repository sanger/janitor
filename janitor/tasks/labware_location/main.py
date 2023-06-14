from os import path
from janitor.db.database import Database
from janitor.helpers.mysql_helpers import load_query
from janitor.helpers.mlwh_helpers import sort_results

wd = path.realpath(path.dirname(__file__))

get_locations_file = "get_labware_locations.sql"
add_to_labware_locations_file = "write_to_labware_locations.sql"

labwhere = {
    "host": "localhost",
    "port": 3000,
    "db_name": "labwhere_prod",
    "username": "root",
    "password": "",
}

mlwh = {
    "host": "localhost",
    "port": 3000,
    "db_name": "unified_warehouse_development",
    "username": "root",
    "password": "",
}


def sync_changes_from_labwhere():
    db_labwhere = Database.create_connection(
        host=labwhere["host"],
        port=labwhere["port"],
        db_name=labwhere["db_name"],
        username=labwhere["username"],
        password=labwhere["password"],
    )

    db_mlwh = Database.create_connection(
        host=mlwh["host"],
        port=mlwh["port"],
        db_name=mlwh["db_name"],
        username=mlwh["username"],
        password=mlwh["password"],
    )

    results = db_labwhere.execute_query(
        load_query(path.join(wd, "sql_queries", get_locations_file))
    )

    column_names = db_labwhere.get_column_names()

    mlwh_entries, invalid_entries = sort_results(results, column_names)

    db_mlwh.write_entries_to_table(
        load_query(path.join(wd, "sql_queries", add_to_labware_locations_file)),
        mlwh_entries,
        5000,
    )

    db_labwhere.close()
    db_mlwh.close()
