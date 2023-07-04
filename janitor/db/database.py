import logging
from typing import Any, Dict, Mapping, Sequence, cast

import mysql.connector as mysql
from mysql.connector.connection_cext import MySQLConnectionAbstract

from janitor.helpers.mysql_helpers import list_of_entries_values
from janitor.types import DbConnectionDetails

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, creds: DbConnectionDetails):
        """Open a MySQL connection to read and write data to tables in a database.

        Arguments:
            creds {DbConnectionDetails}: details for database connection
        """
        self.creds = creds
        self._connection = cast(MySQLConnectionAbstract, None)

    @property
    def connection(self) -> MySQLConnectionAbstract:
        """Database connection, attempt to connect if not connected."""
        if self._connection is not None:
            return self._connection

        logger.info(f"Attempting to connect to {self.creds['host']} on port {self.creds['port']}...")  # type: ignore

        try:
            connection = mysql.connect(
                host=self.creds["host"],
                port=self.creds["port"],
                database=self.creds["db_name"],
                username=self.creds["username"],
                password=self.creds["password"],
            )

            if connection.is_connected():
                logger.info(f"MySQL connection to {self.creds['db_name']} successful!")
                self._connection = cast(MySQLConnectionAbstract, connection)

        except mysql.Error as e:
            logger.error(f"Exception on connecting to MySQL database: {e}")

        return self._connection

    def close(self) -> None:
        """Close connection to database."""
        try:
            if self.connection.is_connected():
                self.connection.close()
        except Exception as e:
            logger.error(f"Exception on closing connection: {e}")

    def execute_query(self, query: str, params: Dict[str, str]) -> Sequence[Any]:
        """Execute an SQL query and return the results and column names.

        Arguments:
            query {str}: SQL query to execute against table
            params {Dict[str, str]}: Additional parameters to inject to SQL query

        Returns:
            results {Sequence[Any]}: list of queried results
        """
        logger.info(f"Executing query: {query}")
        results = cast(Sequence, [])
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
        except Exception as e:
            logger.error(f"Exception on executing query: {e}")

        return results

    def write_entries_to_table(
        self,
        query: str,
        entries: Sequence[Mapping[str, Any]],
        rows_per_query: int,
    ) -> None:
        """Add or update entries to table in batches.

        Arguments:
            query {str}: SQL query to execute against table
            entries {Sequence[Mapping[str, Any]]}: list of parsed entries to add to table
            rows_per_query {int}: number of rows per batch
        """
        num_entries = len(entries)
        index = 0

        try:
            with self.connection.cursor() as cursor:
                self.connection.start_transaction()

                while index < num_entries:
                    entries_batch = list_of_entries_values(entries[index : index + rows_per_query])  # noqa: E203
                    cursor.executemany(query, entries_batch)
                    index += rows_per_query

            self.connection.commit()
        except Exception as e:
            logger.error(f"Exception on writing entries: {e}")
