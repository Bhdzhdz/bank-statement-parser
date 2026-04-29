"""Generic CSV parser.

Expected columns (case-insensitive): date, amount, description.
Optional: currency, reference.
"""

from __future__ import annotations

import csv
import logging
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from bank_statement_parser.exceptions import ParseError
from bank_statement_parser.models import Account, Statement, Transaction

logger = logging.getLogger(__name__)

_REQUIRED_COLUMNS = {"date", "amount", "description"}
_DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y")


def _parse_date(raw: str, path: str) -> date:
    from datetime import datetime

    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    raise ParseError(path, f"Unrecognised date format: '{raw}'")


def _parse_amount(raw: str, path: str) -> Decimal:
    cleaned = raw.strip().replace(",", "").replace(" ", "")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        raise ParseError(path, f"Invalid amount: '{raw}'") from None


class GenericCsvParser:
    """Parses CSV bank statements with date/amount/description columns."""

    def can_parse(self, path: Path) -> bool:
        if path.suffix.lower() != ".csv":
            return False
        try:
            with path.open(newline="", encoding="utf-8-sig") as fh:
                headers = {h.lower().strip() for h in next(csv.reader(fh))}
            return _REQUIRED_COLUMNS.issubset(headers)
        except (OSError, StopIteration):
            return False

    def parse(self, path: Path) -> Statement:
        transactions: list[Transaction] = []
        path_str = str(path)
        try:
            with path.open(newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh)
                # Normalise header names to lowercase
                if reader.fieldnames is None:
                    raise ParseError(path_str, "Empty file")
                reader.fieldnames = [f.lower().strip() for f in reader.fieldnames]
                for row in reader:
                    transactions.append(
                        Transaction(
                            date=_parse_date(row["date"], path_str),
                            amount=_parse_amount(row["amount"], path_str),
                            description=row["description"].strip(),
                            currency=row.get("currency", "MXN").strip(),
                            reference=row.get("reference", "").strip(),
                            raw_data=dict(row),
                        )
                    )
        except OSError as exc:
            raise ParseError(path_str, str(exc)) from exc

        logger.debug("Parsed %d transactions from %s", len(transactions), path)
        account = Account(bank="unknown", account_number="unknown")
        return Statement(account=account, transactions=transactions)
