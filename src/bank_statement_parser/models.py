"""Domain models for bank-statement-parser.

All monetary amounts use Decimal to avoid floating-point rounding errors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class Transaction:
    """A single bank transaction."""

    date: date
    amount: Decimal
    description: str
    currency: str = "MXN"
    reference: str = ""
    raw_data: dict[str, str] = field(default_factory=dict)


@dataclass
class Account:
    """Bank account metadata."""

    bank: str
    account_number: str
    currency: str = "MXN"


@dataclass
class Statement:
    """A parsed bank statement — one account, many transactions."""

    account: Account
    transactions: list[Transaction] = field(default_factory=list)
    start_date: date | None = None
    end_date: date | None = None
