# Monorepo CLAUDE.md Template

Use for multi-package repositories with shared tooling.

## Template

```markdown
# Project

[Monorepo name]: [One-line description of the overall project]

## Tech Stack

- Package Manager: [pnpm/npm/yarn] workspaces
- Build: [Turborepo/Nx/Lerna]
- Language: [TypeScript/etc.]

## Commands

```bash
# Development (all packages)
[dev command]

# Development (specific package)
[dev command for single package]

# Build all
[build command]

# Test all
[test command]

# Lint all
[lint command]
```

## Structure

```
packages/
├── [package-a]/     # [Description]
├── [package-b]/     # [Description]
└── [shared]/        # Shared utilities

apps/
├── [app-a]/         # [Description]
└── [app-b]/         # [Description]

tooling/             # Shared configs
```

## Workspace Rules

### Dependencies
- Internal deps: Use workspace protocol (`workspace:*`)
- External deps: Hoist common deps to root
- Version sync: Keep shared deps aligned

### Package Boundaries
- Each package has single responsibility
- Dependencies flow: apps → packages → shared
- No circular dependencies

## Principles

1. [Top principle]
2. [Second principle]
3. [Third principle]

## Boundaries

- NEVER: [Critical prohibition]
- ASK FIRST: [Approval required]
```

## Variant: pnpm + Turborepo (TypeScript)

```markdown
# Project

[Name]: [Description]

## Tech Stack

- Package Manager: pnpm 8+
- Build: Turborepo
- Language: TypeScript
- Linting: ESLint + Prettier (shared config)
- Testing: Vitest

## Commands

```bash
# Development
pnpm dev                      # All packages
pnpm dev --filter @repo/web   # Specific package

# Build
pnpm build                    # All (cached)
pnpm build --filter @repo/ui  # Specific

# Test
pnpm test                     # All
pnpm test --filter @repo/core # Specific

# Lint
pnpm lint                     # All
pnpm format                   # Format all

# Add dependency
pnpm add -D typescript --filter @repo/web    # To specific
pnpm add -Dw typescript                       # To root

# Clean
pnpm clean                    # Remove all node_modules, dist
```

## Structure

```
.
├── apps/
│   ├── web/                  # Next.js web app
│   │   ├── package.json      # name: @repo/web
│   │   └── ...
│   └── docs/                 # Documentation site
│       └── package.json      # name: @repo/docs
│
├── packages/
│   ├── ui/                   # Shared UI components
│   │   ├── package.json      # name: @repo/ui
│   │   └── src/
│   ├── core/                 # Core business logic
│   │   └── package.json      # name: @repo/core
│   └── config/               # Shared configs
│       ├── eslint/           # @repo/eslint-config
│       ├── typescript/       # @repo/typescript-config
│       └── tailwind/         # @repo/tailwind-config
│
├── turbo.json                # Turborepo config
├── pnpm-workspace.yaml       # Workspace definition
└── package.json              # Root package
```

## Turborepo Configuration

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {}
  }
}
```

## Workspace Rules

### Naming Convention
- Packages: `@repo/[name]`
- Apps use packages, not vice versa
- Config packages: `@repo/[tool]-config`

### Dependency Management
```json
// Internal dependency
{
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/core": "workspace:*"
  }
}
```

### Shared Configuration
```json
// packages/config/typescript/package.json
{
  "name": "@repo/typescript-config",
  "files": ["base.json", "nextjs.json", "react-library.json"]
}

// apps/web/tsconfig.json
{
  "extends": "@repo/typescript-config/nextjs.json"
}
```

## Development Workflow

### Adding a New Package
1. Create directory in `packages/` or `apps/`
2. Initialize `package.json` with `@repo/` prefix
3. Add to `pnpm-workspace.yaml` (if pattern doesn't match)
4. Run `pnpm install` to link

### Cross-Package Changes
1. Make changes in dependency package first
2. Run `pnpm build --filter @repo/changed-pkg`
3. Verify in dependent packages
4. Run full `pnpm test` before committing

## Principles

1. Single source of truth: Shared configs in packages/config
2. Explicit dependencies: No implicit cross-package imports
3. Incremental builds: Leverage Turborepo caching
4. Isolated testing: Each package tests independently

## Boundaries

- NEVER: Import from another package without adding dependency
- NEVER: Duplicate shared configuration
- NEVER: Version mismatch for shared external deps
- ASK FIRST: New top-level packages
- ASK FIRST: Changes to shared configs
- ASK FIRST: New root-level dependencies
```

## Variant: Nx (TypeScript)

```markdown
# Project

[Name]: [Description]

## Tech Stack

- Build: Nx
- Language: TypeScript
- Package Manager: pnpm

## Commands

```bash
# Development
nx serve web                  # Specific app
nx run-many -t serve          # All servable

# Build
nx build web                  # Specific
nx run-many -t build          # All
nx affected -t build          # Changed only

# Test
nx test core                  # Specific
nx affected -t test           # Changed only

# Generate
nx g @nx/react:component Button --project=ui

# Dependency graph
nx graph
```

## Structure

```
.
├── apps/
│   ├── web/                  # Main application
│   └── web-e2e/              # E2E tests
│
├── libs/
│   ├── ui/                   # UI component library
│   ├── core/                 # Core logic
│   └── shared/               # Shared utilities
│
├── nx.json                   # Nx config
├── project.json              # Per-project config (or in each dir)
└── tsconfig.base.json        # Shared TS config
```

## Nx Rules

### Project Boundaries
```json
// nx.json
{
  "extends": "nx/presets/npm.json",
  "@nx/enforce-module-boundaries": [
    "error",
    {
      "depConstraints": [
        { "sourceTag": "type:app", "onlyDependOnLibsWithTags": ["type:lib"] },
        { "sourceTag": "type:lib", "onlyDependOnLibsWithTags": ["type:lib"] }
      ]
    }
  ]
}
```

### Tags
- `type:app` - Applications
- `type:lib` - Libraries
- `scope:shared` - Shared across all
- `scope:feature` - Feature-specific

## Principles

1. Affected commands: Only build/test what changed
2. Computation caching: Local and remote
3. Module boundaries: Enforced via lint rules

## Boundaries

- NEVER: Circular dependencies between libs
- NEVER: Apps importing from other apps
- ASK FIRST: New libs
- ASK FIRST: Changes to module boundaries
```

## Variant: Python (uv workspaces)

```markdown
# Project

[Name]: [Description]

## Tech Stack

- Package Manager: uv workspaces
- Language: Python 3.11+
- Testing: pytest

## Commands

```bash
# Install all
uv sync

# Run in specific package
uv run --package core pytest

# Add dependency to package
uv add requests --package api

# Add dev dependency to root
uv add --dev pytest
```

## Structure

```
.
├── packages/
│   ├── core/
│   │   ├── pyproject.toml    # name = "myproject-core"
│   │   └── src/core/
│   ├── api/
│   │   ├── pyproject.toml    # name = "myproject-api"
│   │   └── src/api/
│   └── cli/
│       ├── pyproject.toml
│       └── src/cli/
│
├── pyproject.toml            # Root workspace
└── uv.lock
```

## Workspace Configuration

```toml
# pyproject.toml (root)
[tool.uv.workspace]
members = ["packages/*"]

# packages/api/pyproject.toml
[project]
name = "myproject-api"
dependencies = [
    "myproject-core",  # Workspace dep
    "fastapi>=0.100",
]

[tool.uv.sources]
myproject-core = { workspace = true }
```

## Principles

1. Explicit deps: Each package declares its needs
2. Workspace protocol: Internal deps via workspace
3. Shared tooling: Root-level dev deps

## Boundaries

- NEVER: Circular dependencies
- NEVER: Direct imports without declared dep
- ASK FIRST: New packages
```
