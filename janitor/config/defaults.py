import os
from janitor.types import DbConnectionDetails

LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

SYNC_JOB_INTERVAL_SEC = 300
SYNC_JOB_OVERLAP_SEC = 10

LABWHERE_DB: DbConnectionDetails = {
    "db_name": "labwhere_prod",
    "host": LOCALHOST,
    "port": 3000,
    "username": "root",
    "password": "",
}

MLWH_DB: DbConnectionDetails = {
    "db_name": "unified_warehouse_development",
    "host": LOCALHOST,
    "port": 3000,
    "username": "root",
    "password": "",
}
