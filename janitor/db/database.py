import logging
import mysql.connector as mysql
from mysql.connector.connection_cext import MySQLConnectionAbstract
from typing import List, Dict, Any, Sequence, cast
from janitor.helpers.mysql_helpers import list_of_entries_values
from janitor.types import DbConnectionDetails

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, creds: DbConnectionDetails):
        """Open a MySQL connection to read and write data to tables in a database.

        Arguments:
            creds {DbConnectionDetails}: details for database connection
        """
        connection = mysql.connect(
            host=creds["host"],
            port=creds["port"],
            database=creds["db_name"],
            username=creds["username"],
            password=creds["password"],
        )

        self.connection = cast(MySQLConnectionAbstract, connection)

        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """Close connection to database."""
        if self.connection.is_connected():
            self.connection.close()
            self.cursor.close()

    def execute_query(self, query: str, params: Dict[str, str]) -> Sequence[Any]:
        """Execute an SQL query and return the results and column names.

        Arguments:
            query {str}: SQL query to execute against table
            params {Dict[str, str]}: Additional parameters to inject to SQL query

        Returns:
            results {List[Any]}: list of queried results
        """
        logger.info(f"Executing query: {query}")
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return results

    def write_entries_to_table(
        self,
        query: str,
        entries: List[Dict[str, Any]],
        rows_per_query: int,
    ) -> None:
        """Add or update entries to table in batches.

        Arguments:
            query {str}: SQL query to execute against table
            values {List[Dict[str, Any]]}: list of parsed entries to add to table
            rows_per_query {str}: number of rows per batch
        """
        self.connection.start_transaction()
        num_entries = len(entries)
        entries_index = 0

        while entries_index < num_entries:
            self.cursor.executemany(
                query,
                list_of_entries_values(entries[entries_index : entries_index + rows_per_query]),  # noqa
            )
            entries_index += rows_per_query

        self.connection.commit()
