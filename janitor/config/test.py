from janitor.types import DbConnectionDetails

from .defaults import *  # noqa: F401, F403
from .logging import LOGGING

# setting here will overwrite those in 'defaults.py'
SYNC_JOB_INTERVAL_SEC = 300

LABWHERE_DB = DbConnectionDetails(
    db_name="janitor_tests_lw_input",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

MLWH_DB = DbConnectionDetails(
    db_name="janitor_tests_mlwh_output",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

# logging config
LOGGING["loggers"]["janitor"]["level"] = "DEBUG"
LOGGING["loggers"]["apscheduler"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["level"] = "DEBUG"
