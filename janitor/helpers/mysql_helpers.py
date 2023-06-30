from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence


def load_query(filepath: Path) -> str:
    """Load query from .sql file.

    Arguments:
        filepath {str}: filepath to .sql file with query

    Returns:
        {str}: SQL query from .sql file
    """
    with open(filepath, "r") as query:
        return query.read()


def parse_entry(entry: List[Any], column_names: List[str]) -> Dict[str, Any]:
    """Parse entry into dictionary form for easier indexing.

    Arguments:
        entry {List[Any]}: data to assign column names to
        column_names {List[str]}: list of column names corresponding to results

    Returns:
        {Dict[str, Any]}: dictionary of column names and corresponding data
    """
    return dict(zip(column_names, entry))


def list_of_entries_values(entries: Sequence[Mapping[str, Any]]) -> List[List[Any]]:
    """
    Unpack the values of parsed entry dictionaries in a batch of entries.

    Arguments:
        entries {Sequence[Mapping[str, Any]]}: entries to be unpacked

    Returns:
        values {List[List[Any]]}: list of unpacked entries
    """
    values = [list(entry.values()) for entry in entries]
    return values
