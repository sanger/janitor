import logging.config
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from janitor.helpers.config_helpers import get_config
from janitor.tasks.labware_location.main import sync_changes_from_labwhere

load_dotenv()

config = get_config()
logging.config.dictConfig(config.LOGGING)

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=False)
    sched.add_job(sync_changes_from_labwhere, "interval", [config], seconds=config.SYNC_JOB_INTERVAL_SEC)
    sched.start()
    while True:
        sleep(300)
