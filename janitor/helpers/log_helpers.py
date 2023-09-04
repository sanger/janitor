import os
from datetime import datetime
from pathlib import Path
from typing import Optional

TMP_FOLDER = Path("./janitor/tmp")


def make_tmp_folder() -> None:
    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)


def save_job_timestamp(job_name: str, timestamp: datetime) -> None:
    make_tmp_folder()
    filepath = TMP_FOLDER / f"{job_name}_latest_timestamp.txt"
    with open(filepath, "w") as file:
        file.write(str(timestamp))


def load_job_timestamp(job_name: str) -> Optional[str]:
    try:
        filepath = TMP_FOLDER / f"{job_name}_latest_timestamp.txt"
        with open(filepath, "r") as file:
            return file.read()
    except:
        return None
