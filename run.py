import logging.config

from apscheduler.schedulers.background import BlockingScheduler
from dotenv import load_dotenv

from janitor.helpers.config_helpers import get_config
from janitor.tasks.labware_location.main import sync_changes_from_labwhere

load_dotenv()

config = get_config()
logging.config.dictConfig(config.LOGGING)

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(sync_changes_from_labwhere, "interval", [config], seconds=config.SYNC_JOB_INTERVAL_SEC)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
