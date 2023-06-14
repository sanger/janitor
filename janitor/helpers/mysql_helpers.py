from typing import List, Dict


def load_query(filepath: str) -> str:
    """Load query from .sql file.

    Arguments:
        filepath {str}: filepath to .sql file with query

    Returns:
        {str}: SQL query from .sql file
    """
    with open(filepath, "r") as query:
        return query.read()


def parse_result(result: List, column_names: List[str]) -> Dict[str, str]:
    """Parse result into dictionary form for easier indexing.

    Arguments:
        result {List}: data to assign column names to
        column_names {List[str]}: list of column names corresponding to results

    Returns:
        {Dict[str, str]}: dictionary of column names and corresponding data
    """
    return dict(zip(column_names, result))
