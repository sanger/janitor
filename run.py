import logging.config

from apscheduler.schedulers.background import BlockingScheduler
from dotenv import load_dotenv

from janitor.helpers.config_helpers import get_config
from janitor.helpers.log_helpers import custom_log
from janitor.tasks.labware_location.main import sync_changes_from_labwhere
from janitor.tasks.sequencing_publisher.main import get_and_publish_sequencing_run_status_changes

load_dotenv()

config = get_config()
logging.config.dictConfig(config.LOGGING)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    sched = BlockingScheduler()

    # labware_location
    sched.add_job(sync_changes_from_labwhere, "interval", [config], seconds=config.SYNC_JOB_INTERVAL_SEC)

    # sequencing_publisher
    sched.add_job(
        get_and_publish_sequencing_run_status_changes,
        "interval",
        [config],
        seconds=config.SEQUENCING_PUBLISHER_JOB_INTERVAL,
    )

    try:
        custom_log(logger, "info", "TASK_DISABLED", f"Job enabled: {config.JOB_ENABLED}")
        if bool(config.JOB_ENABLED):
            sched.start()
        else:
            custom_log(logger, "info", "TASK_DISABLED", "Job not running as it is disabled")
    except (KeyboardInterrupt, SystemExit):
        pass
