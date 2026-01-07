# CLI Tool CLAUDE.md Template

Use for command-line applications and developer tools.

## Template

```markdown
# Project

[One-line description of what the CLI does]

## Tech Stack

- Language: [Python/Rust/Go/Node.js]
- CLI Framework: [typer/clap/cobra/commander]
- Distribution: [PyPI/crates.io/brew/npm]

## Commands

```bash
# Development
[run command]

# Test
[test command]

# Build
[build command]

# Install locally
[local install command]
```

## Structure

```
src/
├── main.[ext]      # Entry point
├── cli.[ext]       # Command definitions
├── commands/       # Subcommand implementations
└── lib/            # Core logic
```

## CLI Design

### Command Structure
```
[tool] [command] [subcommand] [args] [--flags]
```

### Flag Conventions
- Short flags: Single letter (`-v`, `-h`)
- Long flags: Descriptive (`--verbose`, `--help`)
- Boolean flags: No value needed
- Value flags: `--output=file` or `--output file`

### Output Conventions
- Stdout: Normal output (pipeable)
- Stderr: Errors, warnings, progress
- Exit codes: 0 success, 1 error, 2 usage error

## Principles

1. Clear errors: Actionable messages with suggestions
2. Sensible defaults: Work out of the box
3. Composable: Play well with pipes and scripts
4. Discoverable: Good `--help` at every level

## Boundaries

- NEVER: Destructive operations without confirmation
- NEVER: Silent failures
- ASK FIRST: Breaking changes to CLI interface
```

## Variant: Python (Typer)

```markdown
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
```

## Variant: Rust (Clap)

```markdown
# Project

[Description]

## Tech Stack

- Language: Rust
- CLI: clap (derive)
- Error: anyhow / thiserror
- Output: colored, indicatif
- Distribution: crates.io, brew

## Commands

```bash
# Development
cargo run -- --help

# Test
cargo test

# Build release
cargo build --release

# Install locally
cargo install --path .

# Publish
cargo publish
```

## Structure

```
src/
├── main.rs         # Entry, CLI parsing
├── cli.rs          # Clap structs
├── commands/       # Command implementations
│   ├── mod.rs
│   ├── init.rs
│   └── run.rs
├── lib.rs          # Library exports
└── utils/          # Helpers

tests/
└── integration/
```

## CLI Structure

```rust
// cli.rs
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "tool", about = "Description")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
    
    #[arg(short, long, global = true)]
    pub verbose: bool,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Initialize a new project
    Init {
        #[arg(help = "Project name")]
        name: String,
        
        #[arg(short, long, default_value = "default")]
        template: String,
    },
}
```

## Conventions

- Clap derive macros for structure
- anyhow for application errors
- thiserror for library errors
- indicatif for progress bars

## Principles

1. Fast: Release builds optimized
2. Safe: No unwrap in library code
3. Helpful: Clear error messages
4. Portable: Cross-platform support

## Boundaries

- NEVER: panic! in library code
- NEVER: unwrap without comment
- ASK FIRST: New dependencies
- ASK FIRST: Breaking CLI changes
```

## Variant: Node.js (Commander)

```markdown
# Project

[Description]

## Tech Stack

- Runtime: Node.js 20+
- Language: TypeScript
- CLI: Commander.js
- Output: chalk, ora
- Distribution: npm

## Commands

```bash
# Development
pnpm dev -- --help

# Test
pnpm test

# Build
pnpm build

# Link locally
pnpm link --global

# Publish
pnpm publish
```

## Structure

```
src/
├── index.ts        # Entry point
├── cli.ts          # Commander setup
├── commands/       # Command implementations
│   ├── init.ts
│   └── run.ts
├── lib/            # Core logic
└── utils/          # Helpers

bin/
└── cli.js          # Shebang entry
```

## CLI Structure

```typescript
// cli.ts
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command()
  .name('tool')
  .description('Description')
  .version('1.0.0');

program
  .command('init <name>')
  .description('Initialize a new project')
  .option('-t, --template <template>', 'Template to use', 'default')
  .option('-f, --force', 'Overwrite existing')
  .action(async (name, options) => {
    // Implementation
  });

export { program };
```

## Conventions

- Commander for CLI structure
- chalk for colors
- ora for spinners
- Async commands with proper error handling

## Principles

1. Async-first: All commands async
2. Typed: Strict TypeScript
3. Testable: Commands are importable functions
4. Cross-platform: Works on Windows

## Boundaries

- NEVER: Sync file operations
- NEVER: console.log (use chalk)
- ASK FIRST: New commands
- ASK FIRST: Breaking changes
```

## Variant: Go (Cobra)

```markdown
# Project

[Description]

## Tech Stack

- Language: Go 1.21+
- CLI: Cobra
- Config: Viper
- Output: color, spinner
- Distribution: brew, go install

## Commands

```bash
# Development
go run main.go --help

# Test
go test ./...

# Build
go build -o bin/tool

# Install
go install
```

## Structure

```
cmd/
├── root.go         # Root command
├── init.go         # Init subcommand
└── run.go          # Run subcommand

internal/
├── config/         # Configuration
├── core/           # Business logic
└── utils/          # Helpers

main.go             # Entry point
```

## CLI Structure

```go
// cmd/root.go
var rootCmd = &cobra.Command{
    Use:   "tool",
    Short: "Description",
}

// cmd/init.go
var initCmd = &cobra.Command{
    Use:   "init [name]",
    Short: "Initialize a new project",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        template, _ := cmd.Flags().GetString("template")
        return runInit(name, template)
    },
}

func init() {
    initCmd.Flags().StringP("template", "t", "default", "Template to use")
    rootCmd.AddCommand(initCmd)
}
```

## Conventions

- Cobra for CLI structure
- Viper for config files
- RunE (not Run) for error returns
- internal/ for non-exported code

## Principles

1. Fast startup: Lazy initialization
2. Error handling: Return errors, don't os.Exit
3. Config: Support env vars, config files, flags
4. Completion: Support shell completion

## Boundaries

- NEVER: os.Exit in command handlers
- NEVER: Global state
- ASK FIRST: New commands
- ASK FIRST: Breaking changes
```
