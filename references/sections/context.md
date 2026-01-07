# Context Section Guide

The Context section provides technical background Claude needs to work effectively. It typically includes Tech Stack, Directory Structure, and Commands.

## Tech Stack

### Purpose
Tell Claude what technologies are in use so it writes compatible code.

### Structure
```markdown
## Tech Stack

- Language: [Primary language and version]
- Framework: [Main framework]
- Database: [Database system]
- [Other relevant categories]
```

### Guidelines

**Include version constraints when they matter:**
```markdown
## Tech Stack

- Language: Python 3.11+ (uses match statements)
- Framework: FastAPI 0.100+
- Database: PostgreSQL 15 (uses JSONB extensively)
```

**Group related technologies:**
```markdown
## Tech Stack

### Frontend
- Framework: Next.js 14 (App Router)
- Styling: Tailwind CSS 3.4
- State: Zustand

### Backend
- Runtime: Node.js 20
- Database: PostgreSQL + Prisma
- Cache: Redis
```

**Include tooling that affects code:**
```markdown
## Tech Stack

- Formatter: Prettier (2 space indent)
- Linter: ESLint (airbnb config)
- Package Manager: pnpm
```

### Anti-Patterns

**Version numbers without purpose:**
```markdown
- React: 18.2.0
- TypeScript: 5.3.2
```
Unless there's a specific reason (breaking changes, required features), exact patch versions add noise.

**Obvious choices:**
```markdown
- Git: For version control
- VS Code: For editing
```
Claude doesn't need to know your editor.

---

## Directory Structure

### Purpose
Help Claude understand where code lives and what each area does.

### Structure
```markdown
## Structure

```
src/
├── [dir]/     # [responsibility]
├── [dir]/     # [responsibility]
└── [dir]/     # [responsibility]
```
```

### Guidelines

**Show 1-2 levels, annotate purpose:**
```markdown
## Structure

```
src/
├── components/    # Reusable UI components
├── features/      # Feature modules (self-contained)
├── hooks/         # Custom React hooks
├── lib/           # Utilities, helpers
└── types/         # Shared TypeScript types
```
```

**Highlight non-obvious patterns:**
```markdown
## Structure

```
src/
├── features/
│   └── [feature]/
│       ├── api.ts        # tRPC router for this feature
│       ├── components/   # Feature-specific UI
│       └── hooks.ts      # Feature-specific hooks
```

Features are self-contained. Don't import across features.
```

**Note generated or special directories:**
```markdown
## Structure

```
src/
├── generated/     # DO NOT EDIT - Prisma/GraphQL generated
├── __mocks__/     # Jest mocks
└── ...
```
```

### Anti-Patterns

**Too deep:**
```markdown
src/
├── components/
│   ├── ui/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
```
Show patterns, not every file.

**No annotations:**
```markdown
src/
├── components/
├── utils/
├── lib/
├── helpers/
├── common/
```
What's the difference between utils, lib, helpers, and common?

---

## Commands

### Purpose
Provide frequently-used commands so Claude can suggest or run them.

### Structure
```markdown
## Commands

```bash
# Development
pnpm dev

# Test
pnpm test

# Build
pnpm build
```
```

### Guidelines

**Group by purpose:**
```markdown
## Commands

```bash
# Development
pnpm dev              # Start dev server (port 3000)

# Testing
pnpm test             # Run unit tests
pnpm test:e2e         # Run E2E tests (requires running server)
pnpm test:coverage    # Generate coverage report

# Database
pnpm db:migrate       # Run pending migrations
pnpm db:seed          # Seed development data
pnpm db:studio        # Open Prisma Studio

# Quality
pnpm lint             # ESLint check
pnpm format           # Prettier format
pnpm typecheck        # TypeScript check
```
```

**Add context when non-obvious:**
```markdown
```bash
# Requires running `docker compose up` first
pnpm test:integration

# Uses .env.test - never run against production
pnpm db:reset
```
```

**Include common workflows:**
```markdown
## Commands

```bash
# After pulling changes
pnpm install && pnpm db:migrate && pnpm dev

# Before pushing
pnpm lint && pnpm typecheck && pnpm test
```
```

### Anti-Patterns

**Too many commands:**
List the essential ones. If you have 30 scripts, pick the 10 most used.

**No grouping:**
```markdown
## Commands
pnpm dev
pnpm build
pnpm test
pnpm lint
pnpm format
pnpm db:migrate
pnpm db:seed
...
```
Group related commands.

---

## Combined Example

```markdown
## Tech Stack

- Framework: Next.js 14 (App Router)
- Language: TypeScript (strict mode)
- Database: PostgreSQL 15 + Prisma
- Styling: Tailwind CSS
- Testing: Vitest + Playwright

## Structure

```
app/                  # Next.js App Router pages
├── (auth)/           # Auth route group
├── (dashboard)/      # Dashboard route group  
└── api/              # API routes

components/
├── ui/               # shadcn/ui primitives
└── [feature]/        # Feature components

server/
├── actions/          # Server Actions
├── db/               # Prisma client, queries
└── services/         # Business logic

lib/                  # Shared utilities
prisma/               # Schema, migrations
```

## Commands

```bash
# Development
pnpm dev              # Start dev server

# Database
pnpm db:push          # Push schema changes
pnpm db:studio        # Open Prisma Studio

# Quality
pnpm lint && pnpm typecheck && pnpm test

# Build
pnpm build
```
```

## Checklist

### Tech Stack
- [ ] Primary language with version constraints
- [ ] Framework(s) with relevant version info
- [ ] Database/storage systems
- [ ] Key libraries that affect code patterns
- [ ] Tooling that affects formatting/style

### Directory Structure
- [ ] 1-2 levels deep maximum
- [ ] Every directory annotated with purpose
- [ ] Non-obvious patterns explained
- [ ] Generated/protected directories noted

### Commands
- [ ] Grouped by purpose
- [ ] Most-used commands included
- [ ] Context/prerequisites noted where needed
- [ ] Common workflows documented
