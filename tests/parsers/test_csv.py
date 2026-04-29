"""Tests for GenericCsvParser."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from bank_statement_parser.exceptions import ParseError
from bank_statement_parser.parsers.csv import GenericCsvParser


@pytest.fixture
def parser() -> GenericCsvParser:
    return GenericCsvParser()


def test_can_parse_valid_csv(sample_csv: Path, parser: GenericCsvParser) -> None:
    assert parser.can_parse(sample_csv) is True


def test_cannot_parse_non_csv(tmp_path: Path, parser: GenericCsvParser) -> None:
    f = tmp_path / "data.json"
    f.write_text("{}")
    assert parser.can_parse(f) is False


def test_cannot_parse_csv_missing_columns(
    tmp_path: Path, parser: GenericCsvParser
) -> None:
    f = tmp_path / "bad.csv"
    f.write_text("col1,col2\n1,2\n")
    assert parser.can_parse(f) is False


def test_parse_returns_correct_count(
    sample_csv: Path, parser: GenericCsvParser
) -> None:
    statement = parser.parse(sample_csv)
    assert len(statement.transactions) == 2


def test_parse_amounts_are_decimal(sample_csv: Path, parser: GenericCsvParser) -> None:
    statement = parser.parse(sample_csv)
    for tx in statement.transactions:
        assert isinstance(tx.amount, Decimal)


def test_parse_first_transaction(sample_csv: Path, parser: GenericCsvParser) -> None:
    statement = parser.parse(sample_csv)
    tx = statement.transactions[0]
    assert tx.description == "OXXO Store"
    assert tx.amount == Decimal("-120.50")
    assert tx.currency == "MXN"


def test_parse_invalid_amount(tmp_path: Path, parser: GenericCsvParser) -> None:
    f = tmp_path / "bad_amount.csv"
    f.write_text("date,amount,description\n2024-01-01,NOT_A_NUMBER,test\n")
    with pytest.raises(ParseError):
        parser.parse(f)


def test_parse_invalid_date(tmp_path: Path, parser: GenericCsvParser) -> None:
    f = tmp_path / "bad_date.csv"
    f.write_text("date,amount,description\nNOT_A_DATE,100.00,test\n")
    with pytest.raises(ParseError):
        parser.parse(f)


def test_parse_fixture_file(fixtures_dir: Path, parser: GenericCsvParser) -> None:
    """Smoke test against the checked-in fixture file."""
    statement = parser.parse(fixtures_dir / "sample.csv")
    assert len(statement.transactions) == 5
