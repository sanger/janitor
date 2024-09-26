import logging
import time
from datetime import datetime

from janitor.db.database import Database
from janitor.helpers.log_helpers import custom_log
from janitor.helpers.mlwh_helpers import sort_results
from janitor.tasks.labware_location.sql_queries.sql_queries import (
    GET_LATEST_TIMESTAMP_QUERY,
    GET_LOCATIONS_QUERY,
    WRITE_TO_LABWARE_LOCATION_QUERY,
)

logger = logging.getLogger(__name__)


def sync_changes_from_labwhere(config):
    if not bool(config.JOB_ENABLED):
        custom_log(logger, "info", "TASK_START", "Not starting because the job is disabled")
        return
    start = time.time()
    custom_log(logger, "info", "TASK_START", "Starting sync labware locations task...")
    db_labwhere = Database(config.LABWHERE_DB)
    db_mlwh = Database(config.MLWH_DB)

    try:
        latest_timestamp = db_mlwh.execute_query(GET_LATEST_TIMESTAMP_QUERY, {})[0][0]
    except Exception as e:
        custom_log(logger, "error", "TASK_EXCEPTION", f"Exception on querying labware_location: {e}")
        raise

    latest_timestamp = latest_timestamp or datetime.min

    results = db_labwhere.execute_query(
        GET_LOCATIONS_QUERY,
        {"latest_timestamp": latest_timestamp},
    )

    mlwh_entries, invalid_entries = sort_results(results)

    if invalid_entries:
        for entry in invalid_entries:
            custom_log(logger, "error", "TASK_ERROR", f"Found invalid entry: {entry}")

    custom_log(logger, "info", "TASK_PROGRESS", f"Updating {len(mlwh_entries)} rows...")
    db_mlwh.write_entries_to_table(
        WRITE_TO_LABWARE_LOCATION_QUERY,
        mlwh_entries,
        5000,
    )

    custom_log(logger, "info", "TASK_PROGRESS", "Closing connections to databases...")
    db_labwhere.close()
    db_mlwh.close()
    custom_log(logger, "info", "TASK_SUCCESS", "Task successful!")
    custom_log(logger, "info", "TASK_COMPLETE", f"Task complete in {round(time.time() - start, 2)}s")
