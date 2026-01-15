# Project

Claude MD Builder: CLI tool to generate optimized CLAUDE.md files for Claude Code projects.

## Tech Stack

- Language: Python 3.11+
- CLI: Typer
- Output: Rich
- Build System: Hatchling
- Distribution: PyPI

## Commands

```bash
# Development
python3 -m src.claude_builder.cli --help

# Test
python3 -m pytest

# Build
python3 -m pip install -e .

# Validate CLAUDE.md
claude-builder validate .
```

## Structure

```
src/claude_builder/
├── analyzer.py     # Project analysis logic
├── validator.py    # CLAUDE.md validation logic
├── cli.py          # CLI entry point and Typer app
└── resources/      # Templates and section guides
```

## Principles

1. Concise > Comprehensive: Keep CLAUDE.md short and token-efficient.
2. Rich output: Always use Rich for CLI feedback.
3. Type safety: Use type hints for all functions.
4. Testable: Ensure logic is separable from CLI prompts.

## Boundaries

- NEVER: Print without Rich (use console).
- NEVER: Commit secrets or API keys.
- ASK FIRST: Changes to template structures.
- ASK FIRST: New external dependencies.