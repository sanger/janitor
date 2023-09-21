import os
from datetime import datetime
from pathlib import Path
from typing import Optional

TMP_FOLDER = Path("./janitor/tmp")


def make_tmp_folder(tmp_folder_path: Path) -> None:
    """
    Make tmp folder if it doesn't exist.

    Parameters:
        tmp_folder_path {Path}: Path to tmp folder
    """
    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)


def save_job_timestamp(tmp_folder_path: Path, job_name: str, timestamp: datetime) -> None:
    """
    Save timestamp of last time job was run.

    Parameters:
        tmp_folder_path {Path}: Path to tmp folder
        job_name {str}: Name of job
        timestamp {datetime}: Timestamp to write in text file
    """
    make_tmp_folder(tmp_folder_path)
    filepath = tmp_folder_path / f"{job_name}_latest_timestamp.txt"
    with open(filepath, "w") as file:
        file.write(str(timestamp))


def load_job_timestamp(tmp_folder_path: Path, job_name: str) -> Optional[str]:
    """
    Load timestamp of last job run.

    Parameters:
        tmp_folder_path {Path}: Path to tmp folder
        job_name {str}: Name of job

    Returns:
        {Optional[str]}: Timestamp of last job run
    """
    try:
        filepath = tmp_folder_path / f"{job_name}_latest_timestamp.txt"
        with open(filepath, "r") as file:
            return file.read()
    except Exception:
        return None
