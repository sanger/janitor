from pathlib import Path

from janitor.helpers.mysql_helpers import load_query

SQL_FOLDER_PATH = Path("./janitor/tasks/sequencing_publisher/sql_queries")

GET_RUN_STATUS_CHANGES_FILE = "get_run_status_changes.sql"
GET_RUN_STATUS_CHANGES_QUERY = load_query(SQL_FOLDER_PATH / GET_RUN_STATUS_CHANGES_FILE)
