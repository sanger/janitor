import os
from datetime import datetime
from pathlib import Path
from typing import Optional

TMP_FOLDER = Path("./janitor/tmp")


def make_tmp_folder() -> None:
    """
    Make tmp folder if it doesn't exist.
    """
    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)


def save_job_timestamp(job_name: str, timestamp: datetime) -> None:
    """
    Save timestamp of last time job was run.
    """
    make_tmp_folder()
    filepath = TMP_FOLDER / f"{job_name}_latest_timestamp.txt"
    with open(filepath, "w") as file:
        file.write(str(timestamp))


def load_job_timestamp(job_name: str) -> Optional[str]:
    """
    Load timestamp of last job run.

    Returns:
        {Optional[str]}: Timestamp of last job run
    """
    try:
        filepath = TMP_FOLDER / f"{job_name}_latest_timestamp.txt"
        with open(filepath, "r") as file:
            return file.read()
    except Exception:
        return None
