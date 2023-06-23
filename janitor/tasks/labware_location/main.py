import logging
import time
from janitor.tasks.labware_location.sql_queries.sql_queries import GET_LOCATIONS_QUERY, WRITE_TO_LABWARE_LOCATION_QUERY
from janitor.db.database import Database
from janitor.helpers.mlwh_helpers import sort_results

logger = logging.getLogger(__name__)


def sync_changes_from_labwhere(config):
    start = time.time()
    logger.info("Starting sync labware locations task...")
    db_labwhere = Database(config.LABWHERE_DB)
    db_mlwh = Database(config.MLWH_DB)

    results = db_labwhere.execute_query(
        GET_LOCATIONS_QUERY,
        {"interval": str(config.SYNC_JOB_INTERVAL_SEC + config.SYNC_JOB_OVERLAP_SEC)},
    )

    mlwh_entries, invalid_entries = sort_results(results)

    if invalid_entries:
        for entry in invalid_entries:
            logger.error(f"Found invalid entry: {entry}")

    logger.info(f"Updating {len(mlwh_entries)} rows...")
    db_mlwh.write_entries_to_table(
        WRITE_TO_LABWARE_LOCATION_QUERY,
        mlwh_entries,
        5000,
    )

    db_labwhere.close()
    db_mlwh.close()
    logger.info(f"Task complete in {round(time.time() - start, 2)}s")
