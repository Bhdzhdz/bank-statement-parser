"""Tests for the parser registry / detect_and_parse dispatcher."""

from __future__ import annotations

from pathlib import Path

import pytest

from bank_statement_parser.exceptions import UnsupportedFormatError
from bank_statement_parser.parsers import detect_and_parse


def test_detect_and_parse_csv(sample_csv: Path) -> None:
    statement = detect_and_parse(sample_csv)
    assert len(statement.transactions) == 2


def test_detect_and_parse_unsupported(tmp_path: Path) -> None:
    f = tmp_path / "data.xyz"
    f.write_text("nothing")
    with pytest.raises(UnsupportedFormatError):
        detect_and_parse(f)
