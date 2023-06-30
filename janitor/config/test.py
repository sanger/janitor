from .defaults import *  # noqa: F401, F403

# setting here will overwrite those in 'defaults.py'
SYNC_JOB_INTERVAL_SEC = 300
SYNC_JOB_OVERLAP_SEC = 10

LABWHERE_DB = DbConnectionDetails(  # noqa: F405
    db_name="janitor_tests_lw_input",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

MLWH_DB = DbConnectionDetails(  # noqa: F405
    db_name="janitor_tests_mlwh_output",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="",
)

# logging config
LOGGING["loggers"]["janitor"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["apscheduler"]["level"] = "DEBUG"  # noqa: F405
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F405
