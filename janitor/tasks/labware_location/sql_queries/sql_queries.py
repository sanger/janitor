from pathlib import Path

from janitor.helpers.mysql_helpers import load_query

SQL_FOLDER_PATH = Path("./janitor/tasks/labware_location/sql_queries")


GET_LOCATIONS_FILE = "get_labware_locations.sql"
GET_LOCATIONS_QUERY = load_query(SQL_FOLDER_PATH / GET_LOCATIONS_FILE)

WRITE_TO_LABWARE_LOCATION_FILE = "write_to_labware_locations.sql"
WRITE_TO_LABWARE_LOCATION_QUERY = load_query(SQL_FOLDER_PATH / WRITE_TO_LABWARE_LOCATION_FILE)
