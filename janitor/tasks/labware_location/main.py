import logging
from os import path
from janitor.db.database import Database
from janitor.helpers.mysql_helpers import load_query
from janitor.helpers.mlwh_helpers import sort_results
from janitor.helpers.config_helpers import get_config

config = get_config()

wd = path.realpath(path.dirname(__file__))
logger = logging.getLogger(__name__)

GET_LOCATIONS_FILE = "get_labware_locations.sql"
WRITE_TO_LABWARE_LOCATIONS_FILE = "write_to_labware_locations.sql"


def sync_changes_from_labwhere():
    db_labwhere = Database(config.LABWHERE_DB)
    db_mlwh = Database(config.MLWH_DB)

    results = db_labwhere.execute_query(
        load_query(path.join(wd, "sql_queries", GET_LOCATIONS_FILE)),
        {"interval": str(config.SYNC_JOB_INTERVAL_SEC + config.SYNC_JOB_OVERLAP_SEC)},
    )

    mlwh_entries, invalid_entries = sort_results(results)

    if invalid_entries:
        for entry in invalid_entries:
            logger.warning(f"Found invalid entry: {entry}")

    db_mlwh.write_entries_to_table(
        load_query(path.join(wd, "sql_queries", WRITE_TO_LABWARE_LOCATIONS_FILE)),
        mlwh_entries,
        5000,
    )

    db_labwhere.close()
    db_mlwh.close()
