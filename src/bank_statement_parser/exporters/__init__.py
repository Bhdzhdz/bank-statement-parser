"""Exporter Protocol — all exporters must satisfy this interface."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from bank_statement_parser.models import Statement


class Exporter(Protocol):
    """Protocol that every format-specific exporter must implement."""

    def export(self, statement: Statement, dest: Path) -> None:
        """Write the statement to dest in the target format."""
        ...
