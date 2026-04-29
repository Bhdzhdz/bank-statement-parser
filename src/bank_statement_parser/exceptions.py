"""Custom exceptions for bank-statement-parser."""

from __future__ import annotations


class BankStatementError(Exception):
    """Base exception for all bank-statement-parser errors."""


class ParseError(BankStatementError):
    """Raised when a file cannot be parsed (malformed, truncated, etc.)."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"Failed to parse '{path}': {reason}")
        self.path = path
        self.reason = reason


class UnsupportedFormatError(BankStatementError):
    """Raised when no parser can handle the given file."""

    def __init__(self, path: str) -> None:
        super().__init__(f"No parser found for '{path}'")
        self.path = path
