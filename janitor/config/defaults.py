import os

from janitor.types import DbConnectionDetails, RabbitMQDetails

from .logging import *  # noqa: F401, F403

LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

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

# RabbitMQ
RABBITMQ_DETAILS = RabbitMQDetails(
    USERNAME=os.environ["RABBITMQ_USERNAME"],
    PASSWORD=os.environ["RABBITMQ_PASSWORD"],
    HOST=os.environ["RABBITMQ_HOST"],
    PORT=int(os.environ["RABBITMQ_PORT"]),
    VHOST=os.environ["RABBITMQ_VHOST"],
)

# labware_location
SYNC_JOB_INTERVAL_SEC = 300

# sequencing_publisher
SEQUENCING_PUBLISHER_JOB_INTERVAL = 120

RABBITMQ_SEQUENCING_EXCHANGE = "sanger.psd.sample_status.uat"
RABBITMQ_SEQUENCING_MESSAGE_SCHEMA = "janitor/tasks/sequencing_publisher/message_schemas/sample_sequence_status.avsc"
