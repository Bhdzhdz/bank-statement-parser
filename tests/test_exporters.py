"""Tests for JSON exporter."""

from __future__ import annotations

import json
from pathlib import Path

from bank_statement_parser.exporters.json import JsonExporter
from bank_statement_parser.models import Statement


def test_export_creates_file(sample_statement: Statement, tmp_path: Path) -> None:
    dest = tmp_path / "out.json"
    JsonExporter().export(sample_statement, dest)
    assert dest.exists()


def test_export_valid_json(sample_statement: Statement, tmp_path: Path) -> None:
    dest = tmp_path / "out.json"
    JsonExporter().export(sample_statement, dest)
    data = json.loads(dest.read_text())
    assert "transactions" in data
    assert len(data["transactions"]) == 1


def test_export_decimal_as_string(sample_statement: Statement, tmp_path: Path) -> None:
    dest = tmp_path / "out.json"
    JsonExporter().export(sample_statement, dest)
    data = json.loads(dest.read_text())
    assert data["transactions"][0]["amount"] == "-120.50"


def test_export_date_as_iso(sample_statement: Statement, tmp_path: Path) -> None:
    dest = tmp_path / "out.json"
    JsonExporter().export(sample_statement, dest)
    data = json.loads(dest.read_text())
    assert data["transactions"][0]["date"] == "2024-01-15"
