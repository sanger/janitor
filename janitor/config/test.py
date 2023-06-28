# flake8: noqa
from .defaults import *

# setting here will overwrite those in 'defaults.py'
SYNC_JOB_INTERVAL_SEC = 300
SYNC_JOB_OVERLAP_SEC = 10

LABWHERE_DB: DbConnectionDetails = {  # type: ignore
    "db_name": "janitor_tests_lw_input",
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "",
}

MLWH_DB: DbConnectionDetails = {  # type: ignore
    "db_name": "janitor_tests_mlwh_output",
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "",
}

# logging config
LOGGING["loggers"]["janitor"]["level"] = "DEBUG"
LOGGING["loggers"]["apscheduler"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["level"] = "DEBUG"
