"""Parser Protocol — all parsers must satisfy this interface."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from bank_statement_parser.models import Statement


class Parser(Protocol):
    """Protocol that every format-specific parser must implement.

    Usage::

        class MyBankCsvParser:
            def can_parse(self, path: Path) -> bool: ...
            def parse(self, path: Path) -> Statement: ...
    """

    def can_parse(self, path: Path) -> bool:
        """Return True if this parser can handle the given file."""
        ...

    def parse(self, path: Path) -> Statement:
        """Parse the file and return a Statement.

        Raises:
            ParseError: if the file is malformed or unreadable.
        """
        ...
