# Minimal CLAUDE.md Template

Use this template for simple projects or as a starting point.

## Template

```markdown
# Project

[One-line description of what this project does]

## Tech Stack

- Language: [e.g., TypeScript, Python]
- Framework: [e.g., Next.js, FastAPI]
- Database: [if applicable]

## Commands

```bash
# Development
[dev command]

# Test
[test command]

# Build
[build command]
```

## Structure

```
src/
├── [key-dir-1]/  # [responsibility]
├── [key-dir-2]/  # [responsibility]
└── [key-dir-3]/  # [responsibility]
```

## Principles

1. [Most important principle]
2. [Second principle]
3. [Third principle]

## Boundaries

- NEVER: [critical prohibition]
- ASK FIRST: [approval-required action]
```

## Usage Notes

- **Target size**: 30-50 lines
- **Best for**: Solo projects, prototypes, simple tools
- **Expand when**: Team grows, complexity increases, patterns emerge

## Example: Simple CLI Tool

```markdown
# Project

A CLI tool for converting markdown files to PDF.

## Tech Stack

- Language: Python 3.11+
- Key deps: typer, markdown, weasyprint

## Commands

```bash
# Development
uv run python -m md2pdf --help

# Test
uv run pytest

# Build
uv build
```

## Structure

```
src/md2pdf/
├── cli.py       # Entry point, argument parsing
├── convert.py   # Core conversion logic
└── styles/      # CSS templates for PDF output
```

## Principles

1. Clear error messages with actionable suggestions
2. Sensible defaults, extensive customization via flags
3. No external network calls without explicit flag

## Boundaries

- NEVER: Overwrite input files
- ASK FIRST: Operations affecting >10 files
```
