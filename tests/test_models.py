"""Tests for domain models."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from bank_statement_parser.models import Account, Statement, Transaction


def test_transaction_defaults() -> None:
    tx = Transaction(
        date=date(2024, 1, 1), amount=Decimal("100.00"), description="test"
    )
    assert tx.currency == "MXN"
    assert tx.reference == ""
    assert tx.raw_data == {}


def test_statement_empty_by_default(sample_account: Account) -> None:
    stmt = Statement(account=sample_account)
    assert stmt.transactions == []
    assert stmt.start_date is None
    assert stmt.end_date is None


def test_statement_with_transactions(sample_statement: Statement) -> None:
    assert len(sample_statement.transactions) == 1
    assert sample_statement.transactions[0].amount == Decimal("-120.50")
