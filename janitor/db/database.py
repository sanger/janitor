import logging
from typing import Any, Dict, Mapping, Optional, Sequence, cast

import mysql.connector as mysql
from mysql.connector.connection_cext import MySQLConnectionAbstract
from mysql.connector.errors import DatabaseError

from janitor.helpers.log_helpers import custom_log
from janitor.helpers.mysql_helpers import list_of_entries_values
from janitor.types import DbConnectionDetails

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, creds: DbConnectionDetails, autocommit: bool = True):
        """Open a MySQL connection to read and write data to tables in a database.

        Arguments:
            creds {DbConnectionDetails}: details for database connection
        """
        self.creds = creds
        self.autocommit = autocommit
        self._connection: Optional[MySQLConnectionAbstract] = None

    @property
    def connection(self) -> Optional[MySQLConnectionAbstract]:
        """Database connection, attempt to connect if not connected."""
        if self._connection is not None:
            return self._connection

        custom_log(
            logger,
            "info",
            "DATABASE_CONNECTION",
            f"Attempting to connect to {self.creds['host']} on port {self.creds['port']}...",
        )

        try:
            connection = mysql.connect(
                host=self.creds["host"],
                port=self.creds["port"],
                database=self.creds["db_name"],
                username=self.creds["username"],
                password=self.creds["password"],
                autocommit=self.autocommit,
            )

            if connection.is_connected():
                custom_log(
                    logger, "info", "DATABASE_CONNECTION", f"MySQL connection to {self.creds['db_name']} successful!"
                )
                self._connection = cast(MySQLConnectionAbstract, connection)
            else:
                custom_log(logger, "error", "DATABASE_ERROR", f"MySQL connection to {self.creds['db_name']} failed!")

        except mysql.Error as e:
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on connecting to MySQL database: {e}")

        return self._connection

    def close(self) -> None:
        """Close connection to database."""
        try:
            if self._connection is not None and self._connection.is_connected():
                self._connection.close()
        except Exception as e:
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on closing connection: {e}")

    def execute_query(self, query: str, params: Mapping[str, Any]) -> Sequence[Any]:
        """Execute an SQL query and return the results and column names.

        Arguments:
            query {str}: SQL query to execute against table
            params {Mapping[str, Any]}: Additional parameters to inject to SQL query

        Returns:
            results {Sequence[Any]}: list of queried results
        """
        results = cast(Sequence, [])

        if not self.connection:
            err = DatabaseError("Not connected to database!")
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on executing query: {err}")
            raise err

        custom_log(logger, "info", "DATABASE_QUERY", f"Executing query: {query}")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
        except Exception as err:
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on executing query: {err}")

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

        if not self.connection:
            err = DatabaseError("Not connected to database!")
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on writing entries: {err}")
            raise err

        try:
            self.connection.start_transaction()
            with self.connection.cursor() as cursor:
                while index < num_entries:
                    entries_batch = list_of_entries_values(entries[index : index + rows_per_query])
                    cursor.executemany(query, entries_batch)
                    index += rows_per_query

            self.connection.commit()
        except Exception as err:
            custom_log(logger, "error", "DATABASE_EXCEPTION", f"Exception on writing entries: {err}")
