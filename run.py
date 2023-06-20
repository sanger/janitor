import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from janitor.helpers.config_helpers import get_config

config = get_config()
logging.config.dictConfig(config.LOGGING)

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=False)
    sched.add_job(
        sync_changes_from_labwhere, "interval", seconds=config.SYNC_JOB_INTERVAL_SEC
    )
    sched.start()
    while True:
        sleep(300)
