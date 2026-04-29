# AGENTS.md — AI Agent Guide for bank-statement-parser

This file provides context, conventions, and guardrails for AI coding agents
(GitHub Copilot, Claude, Cursor, etc.) working in this repository.

---

## Project Purpose

A Python library/CLI that parses bank statements from various formats (CSV, PDF, OFX, etc.)
and normalises them into a consistent transaction model.

---

## Key Commands

Always use `uv run` to execute tools — do **not** activate the venv manually.

| Task              | Command                          |
|-------------------|----------------------------------|
| Run tests         | `uv run pytest`                  |
| Lint (check only) | `uv run ruff check .`            |
| Lint + auto-fix   | `uv run ruff check --fix .`      |
| Format            | `uv run ruff format .`           |
| Type check        | `uv run ty check`                |
| Commit (guided)   | `uv run cz commit`               |
| Run pre-commit    | `uv run pre-commit run --all-files` |

---

## Architecture

```
bank-statement-parser/
├── main.py              # Entry point / CLI
├── tests/               # pytest test suite
├── pyproject.toml       # Single source of truth for deps and tool config
├── .pre-commit-config.yaml
└── AGENTS.md            # This file
```

As the project grows, organise code under a `src/bank_statement_parser/` package:

```
src/bank_statement_parser/
├── __init__.py
├── parsers/             # One module per bank format (csv, pdf, ofx…)
├── models.py            # Pydantic/dataclass transaction models
└── exporters/           # Output formats (JSON, CSV, ledger…)
```

---

## Coding Conventions

- **Python ≥ 3.13**; use modern syntax (`match`, `|` union types, etc.).
- **Type-annotate everything** — `uv run ty check` must pass before committing.
- **No `print()` in library code** — use `logging` or raise exceptions.
- **Use `pathlib.Path`** instead of `os.path` (ruff rule PTH enforces this).
- **No secrets in code** — API keys, passwords, and tokens must come from env vars.
- **One parser per file format** — keep parsers small and focused.
- **Tests are mandatory** — every public function needs at least one test.

---

## Commit Message Convention (Conventional Commits)

The pre-commit hook enforces this format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`.

Examples:
```
feat(parser): add CSV parser for HSBC statements
fix(models): handle missing transaction date field
test(csv): add edge case for empty files
chore(deps): upgrade ruff to 0.16.0
```

---

## DO / DON'T

### ✅ DO
- Run `uv run pre-commit run --all-files` before opening a PR.
- Add a test for every bug fix and new feature.
- Annotate all function signatures with types.
- Keep parser logic stateless and pure where possible.
- Use `decimal.Decimal` (not `float`) for monetary values.

### ❌ DON'T
- Don't bypass hooks with `git commit --no-verify`.
- Don't add `print()` to library code (use `logging`).
- Don't hardcode file paths — use `pathlib.Path` and accept them as arguments.
- Don't store real bank data in the repository.
- Don't use `Any` as a type annotation without a comment explaining why.
- Don't add dependencies without updating `pyproject.toml` via `uv add`.

---

## Running Checks Locally

```bash
# Full quality gate (same as CI)
uv run pre-commit run --all-files

# Quick feedback loop during development
uv run ruff check --fix . && uv run ruff format . && uv run ty check && uv run pytest
```

---

## Adding a New Parser

1. Create `src/bank_statement_parser/parsers/<bank>_<format>.py`
2. Implement a function `parse(path: Path) -> list[Transaction]`
3. Add tests in `tests/parsers/test_<bank>_<format>.py`
4. Register it in `src/bank_statement_parser/parsers/__init__.py`
5. Commit with `feat(parser): add <bank> <format> parser`
