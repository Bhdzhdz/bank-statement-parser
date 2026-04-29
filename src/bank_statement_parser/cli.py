"""CLI entry point."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from bank_statement_parser import __version__
from bank_statement_parser.parsers import detect_and_parse

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Parse a bank statement file and print a summary."""
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(f"bank-statement-parser {__version__}")
        print("Usage: bsp <path-to-statement>")
        return 0

    path = Path(args[0])
    statement = detect_and_parse(path)
    count = len(statement.transactions)
    print(f"Parsed {count} transaction(s) from {path}")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
