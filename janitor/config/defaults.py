import os
from pathlib import Path

from janitor.types import DbConnectionDetails, RabbitMQDetails

from .logging import *  # noqa: F401, F403

LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

JANITOR_TMP_FOLDER_PATH = Path("./janitor/tmp")

# Databases
LABWHERE_DB = DbConnectionDetails(
    db_name="labwhere_prod",
    host=LOCALHOST,
    port=3000,
    username="root",
    password="",
)

MLWH_DB = DbConnectionDetails(
    db_name="unified_warehouse_development",
    host=LOCALHOST,
    port=3000,
    username="root",
    password="",
)

MLWH_EVENTS_DB = DbConnectionDetails(
    db_name="mlwh_events",
    host=LOCALHOST,
    port=3000,
    username="root",
    password="",
)

# RabbitMQ
RABBITMQ_DETAILS = RabbitMQDetails(
    USERNAME=os.environ.get("RABBITMQ_USERNAME", "rabbitmq_test_username"),
    PASSWORD=os.environ.get("RABBITMQ_PASSWORD", "rabbitmq_test_password"),
    HOST=os.environ.get("RABBITMQ_HOST", "rabbitmq_test_host"),
    PORT=int(os.environ.get("RABBITMQ_PORT", 5672)),
    VHOST=os.environ.get("RABBITMQ_VHOST", "rabbitmq_test_vhost"),
)

# labware_location
SYNC_JOB_INTERVAL_SEC = 300

# sequencing_publisher
SEQUENCING_PUBLISHER_JOB_NAME = "sequencing_publisher"
SEQUENCING_PUBLISHER_JOB_INTERVAL = 600
SEQUENCING_PUBLISHER_MESSAGES_BATCH_SIZE = 100
SEQUENCING_PUBLISHER_RUN_STATUS_QUERY = "./janitor/tasks/sequencing_publisher/sql_queries/get_run_status_changes.sql"

RABBITMQ_SEQUENCING_EXCHANGE = "sanger.psd.sample_status.uat"
RABBITMQ_SEQUENCING_MESSAGE_SCHEMA = "janitor/tasks/sequencing_publisher/message_schemas/sample_sequence_status.avsc"
