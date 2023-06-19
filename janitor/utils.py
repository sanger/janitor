import os
import sys
from logging import Filter
from typing import Iterable


class PackagePathFilter(Filter):
    """Subclass of logging Filter class which provides two log record helpers, namely:

    - relativepath: the relative path to the python module, this allows you to click on the path and line number from
    a terminal and open the source at the exact line in an IDE.
    - relative_path_and_lineno: a concatenation of `relativepath` and `lineno` to easily format the record helper to a
    certain length.

    Based heavily on https://stackoverflow.com/a/52582536/15200392
    """

    def filter(self, record):
        pathname = record.pathname

        record.relativepath = None
        record.relative_path_and_lineno = None

        abs_sys_paths: Iterable[str] = map(os.path.abspath, sys.path)

        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                record.relative_path_and_lineno = (
                    f"{record.relativepath}:{record.lineno}"
                )

                break

        return True
