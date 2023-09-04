from janitor.types import DbConnectionDetails, RabbitMQDetails

from .defaults import *  # noqa: F401, F403
from .logging import LOGGING

# setting here will overwrite those in 'defaults.py'
# Databases
LABWHERE_DB = DbConnectionDetails(
    db_name="janitor_tests_lw",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

MLWH_DB = DbConnectionDetails(
    db_name="janitor_tests_mlwh",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

# RabbitMQ
RABBITMQ_DETAILS = RabbitMQDetails(
    USERNAME="rabbitmq_test_username",
    PASSWORD="rabbitmq_test_password",
    HOST="rabbitmq_test_host",
    PORT=5672,
    VHOST="rabbitmq_test_vhost",
)

# labware_location
SYNC_JOB_INTERVAL_SEC = 300
SEQUENCING_PUBLISHER_MESSAGES_BATCH_SIZE = 10

# sequencing_publisher
SEQUENCING_PUBLISHER_JOB_NAME = "sequencing_publisher"
SEQUENCING_PUBLISHER_JOB_INTERVAL = 120

RABBITMQ_SEQUENCING_EXCHANGE = "sanger.psd.sample_status.uat"
RABBITMQ_SEQUENCING_MESSAGE_SCHEMA = "janitor/tasks/sequencing_publisher/message_schemas/sample_sequence_status.avsc"

# logging config
LOGGING["loggers"]["janitor"]["level"] = "DEBUG"
LOGGING["loggers"]["apscheduler"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["level"] = "DEBUG"
