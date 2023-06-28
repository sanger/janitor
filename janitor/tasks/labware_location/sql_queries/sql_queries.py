from os import path

from janitor.helpers.mysql_helpers import load_query

wd = path.realpath(path.dirname(__file__))


GET_LOCATIONS_FILE = "get_labware_locations.sql"
GET_LOCATIONS_QUERY = load_query(path.join(wd, GET_LOCATIONS_FILE))

WRITE_TO_LABWARE_LOCATION_FILE = "write_to_labware_locations.sql"
WRITE_TO_LABWARE_LOCATION_QUERY = load_query(path.join(wd, WRITE_TO_LABWARE_LOCATION_FILE))
