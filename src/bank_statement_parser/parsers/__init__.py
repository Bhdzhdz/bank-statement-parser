"""Parser registry and auto-dispatch."""

from __future__ import annotations

from pathlib import Path

from bank_statement_parser.exceptions import UnsupportedFormatError
from bank_statement_parser.models import Statement
from bank_statement_parser.parsers.csv import GenericCsvParser

# All registered parsers — order determines priority
_PARSERS = [
    GenericCsvParser(),
]


def detect_and_parse(path: Path) -> Statement:
    """Auto-detect the file format and parse it.

    Raises:
        UnsupportedFormatError: if no registered parser handles the file.
    """
    for parser in _PARSERS:
        if parser.can_parse(path):
            return parser.parse(path)
    raise UnsupportedFormatError(str(path))
