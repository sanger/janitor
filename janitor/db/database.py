import mysql.connector as mysql
from typing import List, Dict


class Database:
    def __init__(
        self, host: str, port: int, db_name: str, username: str, password: str
    ):
        """Open a MySQL connection to read and write data to tables in a database.

        Arguments:
            host {str}: host name for connection
            port {int}: port to connect to
            db_name {str}: name of database
            username {str}: username for connection
            password {str}: password for connection
        """
        self.connection = mysql.connect(host=host, database=db_name, user=username)

        self.cursor = self.connection.cursor()

    @classmethod
    def create_connection(
        cls, host: str, port: int, db_name: str, username: str, password: str
    ) -> "Database":
        """Create a MySQL connection to a database.

        Arguments:
            host {str}: host name for connection
            port {int}: port to connect to
            db_name {str}: name of database
            username {str}: username for connection
            password {str}: password for connection
        """
        return cls(host, port, db_name, username, password)

    def close(self) -> None:
        """Close connection to database."""
        if self.connection.is_connected():
            self.connection.close()
            self.cursor.close()

    def get_column_names(self) -> List[str]:
        """Retrieve list of column names in cursor.

        Returns:
            {List[str]}: list of column names
        """
        return next(zip(*self.cursor.description))

    def execute_query(self, query: str) -> List[List]:
        """Execute an SQL query and return the results and column names.

        Arguments:
            query {str}: SQL query to execute against table

        Returns:
            results {List[List]}: list of queried results
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def write_entries_to_table(
        self,
        query: str,
        values: List[Dict[str, str]],
        rows_per_query: int,
    ) -> None:
        """Add or update entries to table in batches.

        Arguments:
            query {str}: SQL query to execute against table
            values {List[Dict[str, str]]}: list of parsed entries to add to table
            rows_per_query {str}: number of rows per batch
        """
        self.connection.start_transaction()
        num_values = len(values)
        values_index = 0

        while values_index < num_values:
            self.cursor.executemany(
                query,
                values[values_index : values_index + rows_per_query],
            )
            values_index += rows_per_query

        self.connection.commit()
