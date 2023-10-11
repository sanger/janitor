import logging
import time
from datetime import date, datetime
from typing import Any, Sequence

from janitor.db.database import Database
from janitor.helpers.log_helpers import custom_log, load_job_timestamp, save_job_timestamp
from janitor.helpers.mlwh_helpers import make_sample_sequence_message_dicts
from janitor.helpers.mysql_helpers import load_query
from janitor.rabbitmq.rabbit import Rabbit

logger = logging.getLogger(__name__)


def get_and_publish_sequencing_run_status_changes(config):
    start = time.time()

    custom_log(logger, "info", "TASK_START", "Starting sequencing publisher task...")

    # Get sample sequence run changes
    db_mlwh = Database(config.MLWH_DB)

    GET_RUN_STATUS_CHANGES_QUERY = load_query(config.SEQUENCING_PUBLISHER_RUN_STATUS_QUERY)

    run_status_changes: Sequence[Any] = []

    latest_timestamp = load_job_timestamp(config.JANITOR_TMP_FOLDER_PATH, config.SEQUENCING_PUBLISHER_JOB_NAME) or date(
        2023, 8, 21
    )
    save_job_timestamp(config.JANITOR_TMP_FOLDER_PATH, config.SEQUENCING_PUBLISHER_JOB_NAME, datetime.now())

    try:
        run_status_changes = db_mlwh.execute_query(
            GET_RUN_STATUS_CHANGES_QUERY, {"latest_timestamp": str(latest_timestamp)}
        )
        custom_log(logger, "info", "TASK_PROGRESS", "Closing connections to databases...")
        db_mlwh.close()
    except Exception as e:
        custom_log(logger, "error", "TASK_EXCEPTION", f"Exception on querying database: {e}")
        custom_log(logger, "error", "TASK_FAILED", "Task failed!")
        raise

    if not run_status_changes:
        custom_log(logger, "info", "TASK_COMPLETE", "No new changes from MLWH. Skipping task...")
        return

    custom_log(logger, "info", "TASK_PROGRESS", f"Number of changes to publish: {len(run_status_changes)}")

    # Write to RabbitMQ
    sample_message_dicts = make_sample_sequence_message_dicts(run_status_changes)

    try:
        rabbit_connection = Rabbit(config.RABBITMQ_DETAILS)
        last_batch = rabbit_connection.batch_publish_messages(
            exchange=config.RABBITMQ_SEQUENCING_EXCHANGE,
            schema_filepath=config.RABBITMQ_SEQUENCING_MESSAGE_SCHEMA,
            headers={},
            message_dicts=sample_message_dicts,
            batch_size=config.SEQUENCING_PUBLISHER_MESSAGES_BATCH_SIZE,
        )
        if last_batch:
            save_job_timestamp(
                config.JANITOR_TMP_FOLDER_PATH, config.SEQUENCING_PUBLISHER_JOB_NAME, last_batch[0]["latest_timestamp"]
            )
            raise Exception
    except Exception:
        custom_log(logger, "error", "TASK_FAILED", "Task failed!")
        raise
    else:
        rabbit_connection.close()
        custom_log(logger, "info", "TASK_SUCCESS", "Task successful!")

    custom_log(logger, "info", "TASK_COMPLETE", f"Task complete in {round(time.time() - start, 2)}s")
