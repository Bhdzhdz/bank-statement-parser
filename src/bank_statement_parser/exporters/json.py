"""JSON exporter."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from datetime import date
from decimal import Decimal
from pathlib import Path

from bank_statement_parser.models import Statement

logger = logging.getLogger(__name__)


def _default(obj: object) -> str:
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class JsonExporter:
    """Exports a Statement to a JSON file."""

    def export(self, statement: Statement, dest: Path) -> None:
        dest.write_text(
            json.dumps(
                asdict(statement), default=_default, indent=2, ensure_ascii=False
            ),
            encoding="utf-8",
        )
        logger.debug("Exported statement to %s", dest)
