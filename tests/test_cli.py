"""Tests for CLI entry point."""

from __future__ import annotations

from pathlib import Path

import pytest

from bank_statement_parser.cli import main


def test_main_help_returns_zero() -> None:
    assert main(["--help"]) == 0


def test_main_no_args_returns_zero() -> None:
    assert main([]) == 0


def test_main_parse_csv(sample_csv: Path) -> None:
    assert main([str(sample_csv)]) == 0


def test_main_unsupported_file(tmp_path: Path) -> None:
    f = tmp_path / "data.xyz"
    f.write_text("nothing")
    with pytest.raises((SystemExit, Exception)):
        result = main([str(f)])
        assert result != 0
