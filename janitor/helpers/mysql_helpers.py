from typing import List, Dict, Any


def load_query(filepath: str) -> str:
    """Load query from .sql file.

    Arguments:
        filepath {str}: filepath to .sql file with query

    Returns:
        {str}: SQL query from .sql file
    """
    with open(filepath, "r") as query:
        return query.read()


def parse_entry(entry: Dict[str, Any], column_names: List[str]) -> Dict[str, Any]:
    """Parse entry into dictionary form for easier indexing.

    Arguments:
        entry {List[Any]}: data to assign column names to
        column_names {List[str]}: list of column names corresponding to results

    Returns:
        {Dict[str, Any]}: dictionary of column names and corresponding data
    """
    return dict(zip(column_names, entry))


def list_of_entries_values(entries: List[Dict[str, Any]]) -> List[List[Any]]:
    """
    Unpack the values of parsed entry dictionaries in a batch of entries.

    Arguments:
        entries {List[Dict[str, Any]]}: entries to be unpacked

    Returns:
        values {List[List[Any]]}: list of unpacked entries
    """
    values = [list(entry.values()) for entry in entries]
    return values
