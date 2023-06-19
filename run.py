import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from janitor.config.logging import LOGGING

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=False)
    sched.add_job(sync_changes_from_labwhere, "interval", seconds=300)
    sched.start()
    while True:
        sleep(300)
