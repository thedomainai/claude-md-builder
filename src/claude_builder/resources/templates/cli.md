# Project

[Description]

## Tech Stack

- Language: Python 3.11+
- CLI: Typer
- Config: tomli / pydantic-settings
- Output: Rich
- Distribution: PyPI

## Commands

```bash
# Development
uv run python -m [package] --help

# Test
uv run pytest -v

# Build
uv build

# Install locally
uv pip install -e .

# Publish
uv publish
```

## Structure

```
src/[package]/
├── __init__.py
├── __main__.py     # Entry: `python -m [package]`
├── cli.py          # Typer app, commands
├── commands/       # Subcommand modules
│   ├── init.py
│   └── run.py
├── core/           # Business logic
└── utils/          # Helpers

tests/
├── conftest.py
├── test_cli.py
└── test_core/
```

## CLI Structure

```python
# cli.py
import typer
from rich.console import Console

app = typer.Typer(
    name="[tool]",
    help="[Description]",
    no_args_is_help=True,
)
console = Console()

@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("default", "--template", "-t", help="Template to use"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing"),
):
    """Initialize a new project."""
    ...
```

## Conventions

- Typer for CLI structure
- Rich for formatted output
- Click testing for CLI tests
- Type hints on all commands

## Principles

1. Rich output: Colors, tables, progress bars
2. Type safety: Full type hints
3. Testable: Commands return, don't exit
4. Config files: Support pyproject.toml, .toolrc

## Boundaries

- NEVER: Print without Rich (use console)
- NEVER: sys.exit in library code
- ASK FIRST: New top-level commands
- ASK FIRST: Breaking flag changes