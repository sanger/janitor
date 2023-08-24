import logging
import time
from datetime import date
from typing import Any, Sequence

from janitor.db.database import Database
from janitor.helpers.mlwh_helpers import make_sample_sequence_message_dicts
from janitor.rabbitmq.rabbit import Rabbit
from janitor.tasks.sequencing_publisher.sql_queries.sql_queries import GET_RUN_STATUS_CHANGES_QUERY

logger = logging.getLogger(__name__)


def get_and_publish_sequencing_run_status_changes(config):
    start = time.time()
    logger.info("Starting sequencing publisher task...")

    # Get sample sequence run changes
    db_mlwh = Database(config.MLWH_DB)

    run_status_changes: Sequence[Any] = []

    try:
        run_status_changes = db_mlwh.execute_query(
            GET_RUN_STATUS_CHANGES_QUERY, {"latest_timestamp": str(date(2023, 2, 1))}
        )
        logger.info("Closing connections to databases...")
        db_mlwh.close()
    except Exception as e:
        logger.error(f"Exception on querying database: {e}")
        logger.error("Task failed!")
        raise

    if not run_status_changes:
        logger.info("No new changes from MLWH. Skipping task...")
        return

    # Write to RabbitMQ
    sample_message_dicts = make_sample_sequence_message_dicts(run_status_changes)

    try:
        logger.info("Attempting to connect to RabbitMQ...")
        rabbit_connection = Rabbit(config.RABBITMQ_DETAILS)
        for message_dict in sample_message_dicts:
            rabbit_connection.publish_message(
                exchange=config.RABBITMQ_SEQUENCING_EXCHANGE,
                schema_filepath=config.RABBITMQ_SEQUENCING_MESSAGE_SCHEMA,
                headers={},
                message_dicts=[message_dict],
            )
    except Exception as err:
        logger.error(f"Exception on publishing to RabbitMQ: {err}")
        logger.error("Task failed!")
        raise

    logger.info("Task successful!")
    logger.info(f"Task complete in {round(time.time() - start, 2)}s")
