import os

from janitor.types import DbConnectionDetails, RabbitMQDetails

from .logging import *  # noqa: F401, F403

LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

SYNC_JOB_INTERVAL_SEC = 300

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

RABBITMQ_DETAILS = RabbitMQDetails(
    USERNAME=os.environ["RABBITMQ_USERNAME"],
    PASSWORD=os.environ["RABBITMQ_PASSWORD"],
    HOST=os.environ["RABBITMQ_HOST"],
    PORT=int(os.environ["RABBITMQ_PORT"]),
    VHOST=os.environ["RABBITMQ_VHOST"],
)
