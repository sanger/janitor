import os
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Optional


def custom_log(logger: Logger, event_type: str, event_name: str, text: str) -> None:
    """
    Log a message with specified severity and name.

    Parameters:
        logger {Logger}: Logger to use
        event_type {str}: 'info' or 'error'
        event_name {str}: Name of event (TASK_START, TASK_COMPLETE etc.)
        text {str}: Text to log

    Returns:
        msg {str}: Logged message
    """
    if event_type not in ["info", "error"]:
        raise ValueError("Invalid event type. Please specify 'info' or 'error'.")

    if event_type == "info":
        logger.info(f"[{event_name}]")
        logger.info(text)
    else:
        logger.error(f"[{event_name}]")
        logger.error(text)


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
