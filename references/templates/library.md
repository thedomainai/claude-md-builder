# Library/SDK CLAUDE.md Template

Use for reusable libraries, SDKs, and packages.

## Template

```markdown
# Project

[Library name]: [One-line description]

## Tech Stack

- Language: [TypeScript/Python/Rust/etc.]
- Target: [Browser/Node.js/Both/etc.]
- Distribution: [npm/PyPI/crates.io]

## Commands

```bash
# Development
[dev/watch command]

# Test
[test command]

# Build
[build command]

# Docs
[docs generation command]

# Publish
[publish command]
```

## Structure

```
src/
├── index.[ext]     # Public exports
├── core/           # Core functionality
├── utils/          # Internal utilities
└── types.[ext]     # Type definitions
```

## API Design

### Public API
- Exported from index.[ext]
- Documented with JSDoc/docstrings
- Versioned following semver

### Internal API
- Not exported from index
- May change without notice
- Prefixed with _ if exposed

## Principles

1. Minimal API surface: Export only what's needed
2. Backward compatibility: Semver strictly followed
3. Zero/minimal dependencies: Avoid dependency bloat
4. Tree-shakeable: Support dead code elimination

## Boundaries

- NEVER: Breaking changes without major version
- NEVER: Add dependencies without justification
- NEVER: Export internal utilities
- ASK FIRST: New public API additions
- ASK FIRST: New peer dependencies
```

## Variant: TypeScript Library (npm)

```markdown
# Project

[Library name]: [Description]

## Tech Stack

- Language: TypeScript
- Target: Browser + Node.js (ESM + CJS)
- Build: tsup
- Test: Vitest
- Docs: TypeDoc
- Distribution: npm

## Commands

```bash
# Development
pnpm dev              # Watch mode

# Test
pnpm test             # Run tests
pnpm test:coverage    # With coverage

# Build
pnpm build            # Build ESM + CJS + types

# Docs
pnpm docs             # Generate TypeDoc

# Publish
pnpm release          # Version bump + publish
```

## Structure

```
src/
├── index.ts          # Public exports (barrel)
├── core/
│   ├── client.ts     # Main class/functions
│   └── types.ts      # Public types
├── utils/            # Internal utilities
└── errors.ts         # Custom error classes

tests/
├── unit/             # Unit tests
└── integration/      # Integration tests

examples/             # Usage examples
docs/                 # Generated docs
```

## Package Configuration

```json
// package.json (key fields)
{
  "name": "@scope/library",
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist"],
  "sideEffects": false
}
```

## API Design

### Exports Pattern
```typescript
// src/index.ts - Only public API
export { Client } from './core/client';
export type { ClientOptions, Result } from './core/types';
export { LibraryError, ValidationError } from './errors';

// Do NOT export:
// - Internal utilities
// - Implementation details
// - Private types
```

### Naming Conventions
- Classes: PascalCase (`Client`, `Builder`)
- Functions: camelCase (`createClient`, `parseConfig`)
- Types: PascalCase (`ClientOptions`, `Result<T>`)
- Constants: SCREAMING_SNAKE (`DEFAULT_TIMEOUT`)

## Principles

1. Type-first: Types are the documentation
2. ESM-first: ESM primary, CJS for compatibility
3. Zero runtime deps: Bundle what's needed
4. Tree-shakeable: Named exports, sideEffects: false

## Boundaries

- NEVER: Default exports (breaks tree-shaking)
- NEVER: Runtime type checking (TypeScript handles it)
- NEVER: Modify global objects
- NEVER: Console.log in library code
- ASK FIRST: New exports
- ASK FIRST: Any new dependency
```

## Variant: Python Library (PyPI)

```markdown
# Project

[Library name]: [Description]

## Tech Stack

- Language: Python 3.10+
- Build: hatchling
- Test: pytest
- Docs: Sphinx / mkdocs
- Type checking: mypy
- Distribution: PyPI

## Commands

```bash
# Development
uv pip install -e ".[dev]"

# Test
uv run pytest -v
uv run pytest --cov

# Type check
uv run mypy src/

# Docs
uv run mkdocs serve

# Build
uv build

# Publish
uv publish
```

## Structure

```
src/[package]/
├── __init__.py       # Public exports
├── core.py           # Main functionality
├── types.py          # Type definitions
├── exceptions.py     # Custom exceptions
└── _internal/        # Private modules
    └── utils.py

tests/
├── conftest.py
├── test_core.py
└── test_integration/

docs/
examples/
```

## API Design

### Exports Pattern
```python
# src/[package]/__init__.py
from .core import Client, create_client
from .types import ClientOptions, Result
from .exceptions import LibraryError, ValidationError

__all__ = [
    "Client",
    "create_client",
    "ClientOptions",
    "Result",
    "LibraryError",
    "ValidationError",
]
```

### Naming Conventions
- Classes: PascalCase
- Functions: snake_case
- Constants: SCREAMING_SNAKE
- Private: _prefixed

## Principles

1. Type hints: Full coverage, strict mypy
2. Minimal deps: Standard library when possible
3. Pythonic: Follow Python idioms
4. Documented: Docstrings on all public API

## Boundaries

- NEVER: Import from _internal outside package
- NEVER: Print statements (use logging)
- NEVER: Mutable default arguments
- ASK FIRST: New public API
- ASK FIRST: New dependencies
```

## Variant: Rust Crate (crates.io)

```markdown
# Project

[Crate name]: [Description]

## Tech Stack

- Language: Rust
- Edition: 2021
- Test: built-in + proptest
- Docs: rustdoc
- Distribution: crates.io

## Commands

```bash
# Development
cargo build

# Test
cargo test
cargo test --doc        # Doc tests

# Docs
cargo doc --open

# Clippy
cargo clippy -- -D warnings

# Publish
cargo publish
```

## Structure

```
src/
├── lib.rs            # Crate root, public exports
├── client.rs         # Main types
├── error.rs          # Error types
└── internal/         # Private modules
    └── mod.rs

tests/
└── integration/      # Integration tests

examples/             # Example binaries
benches/              # Benchmarks
```

## API Design

### Exports Pattern
```rust
// src/lib.rs
mod client;
mod error;
mod internal;

pub use client::{Client, ClientBuilder};
pub use error::{Error, Result};

// Re-export commonly used traits
pub mod prelude {
    pub use crate::{Client, Error, Result};
}
```

### Naming Conventions
- Types: PascalCase
- Functions: snake_case
- Constants: SCREAMING_SNAKE
- Private: no pub, or pub(crate)

## Principles

1. Safe by default: unsafe only when necessary
2. Zero-cost abstractions: No runtime overhead
3. Documented: /// on all pub items
4. Tested: Unit + doc + integration tests

## Boundaries

- NEVER: Unwrap in library code
- NEVER: Panic in public functions
- NEVER: Unsafe without safety comment
- ASK FIRST: New public API
- ASK FIRST: MSRV changes
```
