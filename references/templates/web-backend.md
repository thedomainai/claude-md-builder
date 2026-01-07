# Web Backend CLAUDE.md Template

Use for API servers, microservices, or backend applications.

## Template

```markdown
# Project

[One-line description of the API/service]

## Tech Stack

- Language: [Python/Node.js/Go/etc.]
- Framework: [FastAPI/Express/Gin/etc.]
- Database: [PostgreSQL/MySQL/MongoDB/etc.]
- ORM: [Prisma/SQLAlchemy/GORM/etc.]
- Auth: [JWT/OAuth/Session/etc.]

## Commands

```bash
# Development
[dev command with hot reload]

# Test
[test command]

# Database
[migration commands]

# Build/Deploy
[build command]
```

## Structure

```
src/
├── api/           # Route handlers
│   └── v1/        # Versioned endpoints
├── models/        # Database models
├── services/      # Business logic
├── middleware/    # Auth, logging, etc.
├── lib/           # Utilities
└── types/         # Type definitions
```

## API Conventions

- RESTful endpoints: `GET /resources`, `POST /resources`, `GET /resources/:id`
- Consistent error responses: `{ error: string, code: string, details?: object }`
- Pagination: `?page=1&limit=20` or cursor-based
- Versioning: URL prefix `/api/v1/`

## Principles

1. Security: Validate all inputs, sanitize outputs
2. Idempotency: Safe retries for non-GET requests
3. Observability: Structured logging, error tracking
4. Performance: Index queries, cache when appropriate

## Boundaries

- NEVER: Raw SQL without parameterization
- NEVER: Secrets in code or logs
- NEVER: Skip input validation
- ASK FIRST: Schema migrations
- ASK FIRST: New external service integrations
- ASK FIRST: Authentication flow changes
```

## Variant: Python FastAPI

```markdown
# Project

[Description]

## Tech Stack

- Language: Python 3.11+
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy 2.0 + Alembic
- Validation: Pydantic v2
- Auth: JWT with python-jose

## Commands

```bash
# Development
uv run uvicorn app.main:app --reload

# Test
uv run pytest -v

# Database
uv run alembic upgrade head      # Apply migrations
uv run alembic revision --autogenerate -m "description"

# Lint
uv run ruff check . && uv run ruff format .
```

## Structure

```
app/
├── main.py           # FastAPI app, middleware
├── api/
│   └── v1/
│       ├── routes/   # Route handlers
│       └── deps.py   # Dependency injection
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── core/
│   ├── config.py     # Settings (pydantic-settings)
│   ├── security.py   # Auth utilities
│   └── database.py   # DB session
└── tests/
    ├── conftest.py   # Fixtures
    └── api/          # API tests
```

## Conventions

- Async by default for I/O operations
- Dependency injection for DB sessions, current user
- Pydantic models for request/response validation
- Service layer for business logic (not in routes)

## Principles

1. Type hints everywhere: Full typing coverage
2. Async-first: Use async def for endpoints
3. Dependency injection: Testable, modular code
4. Schema validation: Pydantic for all I/O

## Boundaries

- NEVER: Business logic in route handlers
- NEVER: Raw SQL (use ORM)
- NEVER: Sync DB calls in async context
- ASK FIRST: New Alembic migrations
- ASK FIRST: Changes to auth flow
```

## Variant: Node.js Express/TypeScript

```markdown
# Project

[Description]

## Tech Stack

- Runtime: Node.js 20+
- Framework: Express
- Language: TypeScript
- Database: PostgreSQL
- ORM: Prisma
- Validation: Zod
- Auth: Passport.js + JWT

## Commands

```bash
# Development
pnpm dev              # ts-node-dev with watch

# Test
pnpm test             # Jest

# Database
pnpm db:migrate       # Prisma migrate
pnpm db:generate      # Generate client
pnpm db:studio        # Prisma Studio

# Build
pnpm build            # TypeScript compile
```

## Structure

```
src/
├── index.ts          # Entry point
├── app.ts            # Express app setup
├── routes/
│   └── v1/           # Versioned routes
├── controllers/      # Request handlers
├── services/         # Business logic
├── middleware/       # Auth, validation, errors
├── lib/
│   ├── prisma.ts     # Prisma client
│   └── logger.ts     # Winston logger
└── types/            # TypeScript types

prisma/
├── schema.prisma     # Database schema
└── migrations/       # Migration history
```

## Conventions

- Controller → Service → Repository pattern
- Zod schemas for request validation
- Centralized error handling middleware
- Structured JSON logging

## Principles

1. Type safety: Strict TypeScript, Prisma types
2. Error handling: Custom error classes, consistent responses
3. Validation: Zod middleware for all inputs
4. Logging: Structured logs, request IDs

## Boundaries

- NEVER: Direct Prisma calls in controllers
- NEVER: Untyped request bodies
- NEVER: Console.log (use logger)
- ASK FIRST: Prisma schema changes
- ASK FIRST: New middleware
```

## Variant: Go Gin

```markdown
# Project

[Description]

## Tech Stack

- Language: Go 1.21+
- Framework: Gin
- Database: PostgreSQL
- ORM: GORM
- Migration: golang-migrate
- Config: Viper

## Commands

```bash
# Development
go run cmd/server/main.go

# Test
go test ./... -v

# Build
go build -o bin/server cmd/server/main.go

# Database
migrate -path migrations -database $DATABASE_URL up
```

## Structure

```
cmd/
└── server/
    └── main.go       # Entry point

internal/
├── api/
│   ├── handler/      # HTTP handlers
│   ├── middleware/   # Gin middleware
│   └── router.go     # Route definitions
├── model/            # GORM models
├── repository/       # Data access
├── service/          # Business logic
└── config/           # Configuration

pkg/                  # Shared utilities
migrations/           # SQL migrations
```

## Conventions

- Handler → Service → Repository layers
- Context propagation for cancellation
- Structured errors with codes
- Interface-based dependencies

## Principles

1. Simplicity: Standard library when sufficient
2. Error handling: Explicit, no panic
3. Concurrency: Context-aware, graceful shutdown
4. Testing: Table-driven tests, interfaces for mocking

## Boundaries

- NEVER: Panic in handlers
- NEVER: Global state
- NEVER: Skip context propagation
- ASK FIRST: New external dependencies
- ASK FIRST: Schema migrations
```
