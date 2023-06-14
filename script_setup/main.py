from os import path
from database import Database
from db_helpers import load_query, sort_results

wd = path.realpath(path.dirname(__file__))

get_locations_file = "get_labware_locations.sql"
add_to_labware_locations_file = "write_to_labware_locations.sql"

labwhere = {
    "host": "localhost",
    "db_name": "labwhere_prod",
    "username": "root",
    "password": "",
}

mlwh = {
    "host": "localhost",
    "db_name": "unified_warehouse_development",
    "username": "root",
    "password": "",
}


if __name__ == "__main__":
    db_labwhere = Database(
        host=labwhere["host"],
        db_name=labwhere["db_name"],
        username=labwhere["username"],
    )

    db_mlwh = Database(
        host=mlwh["host"],
        db_name=mlwh["db_name"],
        username=mlwh["username"],
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

    print(f"\nNumber of bad entries: {len(invalid_entries)}")
    print(invalid_entries)

    db_labwhere.close()
    db_mlwh.close()
