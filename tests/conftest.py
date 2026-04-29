"""Shared pytest fixtures."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from bank_statement_parser.models import Account, Statement, Transaction


@pytest.fixture
def sample_transaction() -> Transaction:
    return Transaction(
        date=date(2024, 1, 15),
        amount=Decimal("-120.50"),
        description="OXXO Store",
        currency="MXN",
        reference="REF001",
    )


@pytest.fixture
def sample_account() -> Account:
    return Account(bank="Test Bank", account_number="0001")


@pytest.fixture
def sample_statement(
    sample_account: Account, sample_transaction: Transaction
) -> Statement:
    return Statement(account=sample_account, transactions=[sample_transaction])


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """A temporary CSV file with synthetic transaction data."""
    csv_file = tmp_path / "statement.csv"
    csv_file.write_text(
        "date,amount,description,currency,reference\n"
        "2024-01-15,-120.50,OXXO Store,MXN,REF001\n"
        "2024-01-16,5000.00,Salary deposit,MXN,REF002\n",
        encoding="utf-8",
    )
    return csv_file


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"
