from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from janitor.tasks.labware_location.main import sync_changes_from_labwhere

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=False)
    sched.add_job(sync_changes_from_labwhere, "interval", seconds=300)
    sched.start()
    while True:
        sleep(300)
