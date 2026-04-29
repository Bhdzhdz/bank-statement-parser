# GitHub Copilot Agent Instructions
# This file is read automatically by GitHub Copilot for repository-specific context.

## Project: bank-statement-parser

A Python library + CLI that parses bank statement files (CSV, PDF, OFX, etc.)
and normalises them into a consistent `Statement` / `Transaction` model.

---

## Architecture

```
src/bank_statement_parser/
├── __init__.py      ← public API (only export via __all__)
├── cli.py           ← CLI — keep thin, just arg parsing + call library code
├── models.py        ← Transaction, Account, Statement (Decimal amounts, never float)
├── exceptions.py    ← ParseError, UnsupportedFormatError
├── parsers/
│   ├── base.py      ← Parser Protocol — ALL parsers must implement can_parse + parse
│   ├── __init__.py  ← registry + detect_and_parse() dispatcher
│   └── csv.py       ← Generic CSV parser (reference implementation)
└── exporters/
    ├── __init__.py  ← Exporter Protocol
    └── json.py      ← JSON exporter (reference implementation)

tests/
├── conftest.py      ← shared fixtures — ALWAYS use these instead of creating new ones
├── fixtures/        ← synthetic sample files (NEVER commit real bank data)
└── parsers/
```

---

## Critical Rules

1. **Always use `Decimal` for money** — never `float`. Import from `decimal`.
2. **Every parser must implement the `Parser` Protocol** (`can_parse` + `parse`).
   Register it in `parsers/__init__.py` `_PARSERS` list.
3. **Every exporter must implement the `Exporter` Protocol** (`export`).
4. **Raise `ParseError` or `UnsupportedFormatError`** — never generic `ValueError`/`Exception`.
5. **No `print()` in library code** — use `logging.getLogger(__name__)`.
6. **Use `pathlib.Path`** everywhere — never `os.path` or raw string paths.
7. **Type-annotate all function signatures** — `uv run ty check` must pass.
8. **Tests are not optional** — new parsers/exporters need tests in `tests/parsers/` or `tests/exporters/`.
9. **Use shared fixtures from `conftest.py`** — don't duplicate fixture logic.
10. **Never commit real bank data** — all `tests/fixtures/` files must be synthetic.

---

## Key Commands

```bash
uv run pytest                          # run tests + coverage
uv run ruff check --fix .              # lint + auto-fix
uv run ruff format .                   # format
uv run ty check                        # type check
uv run pre-commit run --all-files      # full quality gate
```

---

## Adding a New Parser (step-by-step)

1. Create `src/bank_statement_parser/parsers/<bank>_<format>.py`
2. Implement a class with `can_parse(self, path: Path) -> bool` and `parse(self, path: Path) -> Statement`
3. Add synthetic fixture file in `tests/fixtures/`
4. Add tests in `tests/parsers/test_<bank>_<format>.py` — cover happy path + error cases
5. Register in `parsers/__init__.py` `_PARSERS`
6. Commit: `feat(parser): add <bank> <format> parser`

---

## Data Contract (do not change without updating tests)

```python
@dataclass
class Transaction:
    date: date
    amount: Decimal      # negative = debit, positive = credit
    description: str
    currency: str        # ISO 4217, default "MXN"
    reference: str
    raw_data: dict[str, str]
```
