# Full Stack CLAUDE.md Template

Use for projects with both frontend and backend in the same repository.

## Template

```markdown
# Project

[One-line description]

## Tech Stack

### Frontend
- Framework: [Next.js/Nuxt/SvelteKit/etc.]
- Language: TypeScript
- Styling: [Tailwind/etc.]
- State: [Zustand/etc.]

### Backend
- Runtime: [Node.js/Python/etc.]
- Database: [PostgreSQL/etc.]
- ORM: [Prisma/Drizzle/etc.]
- Auth: [NextAuth/Lucia/etc.]

## Commands

```bash
# Development
[single command to start full stack]

# Frontend only
[frontend dev command]

# Backend only
[backend dev command]

# Database
[migration commands]

# Test
[test command]

# Build
[build command]
```

## Structure

```
[Project structure overview]
```

## Architecture

### Data Flow
```
Client → API Routes → Services → Database
              ↓
         Validation (Zod)
```

### Key Boundaries
- Frontend: `app/`, `components/`
- Backend: `server/`, `api/`
- Shared: `lib/`, `types/`

## Conventions

### Frontend
- [Key frontend conventions]

### Backend
- [Key backend conventions]

### Shared
- [Conventions for shared code]

## Principles

1. [Top principle]
2. [Second principle]
3. [Third principle]

## Boundaries

- NEVER: [Critical prohibition]
- ASK FIRST: [Approval required action]
```

## Variant: Next.js Full Stack

```markdown
# Project

[Description]

## Tech Stack

### Frontend
- Framework: Next.js 14 (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Components: shadcn/ui
- State: Zustand (client), TanStack Query (server)

### Backend
- API: Next.js API Routes + Server Actions
- Database: PostgreSQL
- ORM: Prisma
- Auth: NextAuth.js v5
- Validation: Zod

## Commands

```bash
# Development
pnpm dev                    # Start Next.js (frontend + API)

# Database
pnpm db:push               # Push schema changes
pnpm db:migrate            # Create migration
pnpm db:studio             # Open Prisma Studio
pnpm db:seed               # Seed database

# Test
pnpm test                  # Unit tests (Vitest)
pnpm test:e2e              # E2E tests (Playwright)

# Build & Deploy
pnpm build                 # Production build
pnpm start                 # Start production server
```

## Structure

```
app/
├── (auth)/                # Auth pages (login, register)
├── (dashboard)/           # Protected dashboard routes
│   └── settings/
├── api/                   # API routes (when Server Actions insufficient)
│   └── webhooks/
├── layout.tsx             # Root layout
└── page.tsx               # Landing page

components/
├── ui/                    # shadcn/ui primitives
├── forms/                 # Form components
└── [feature]/             # Feature-specific components

server/
├── actions/               # Server Actions
├── db/                    # Prisma client, queries
└── services/              # Business logic

lib/
├── auth.ts                # Auth config
├── utils.ts               # Shared utilities
└── validations/           # Zod schemas

prisma/
├── schema.prisma
└── migrations/
```

## Architecture

### Data Flow
```
Page/Component
    ↓
Server Action (mutation) or Server Component (query)
    ↓
Service Layer (business logic)
    ↓
Prisma (data access)
    ↓
PostgreSQL
```

### Key Decisions
- **Server Actions** for mutations (forms, updates)
- **Server Components** for data fetching
- **API Routes** only for webhooks, external integrations
- **Client Components** only for interactivity

## Conventions

### Frontend
- Server Components by default
- `'use client'` only with justification comment
- Forms use react-hook-form + Server Actions
- Loading states with Suspense boundaries

### Backend
- Server Actions in `server/actions/`
- Business logic in `server/services/`
- Database queries in `server/db/`
- All inputs validated with Zod

### Shared
- Types in `types/` directory
- Zod schemas double as TypeScript types
- Utils in `lib/utils.ts`

## Principles

1. Server-first: Maximize Server Components
2. Type safety: End-to-end Prisma + Zod types
3. Colocation: Keep related code together
4. Security: Validate all inputs, check auth in Server Actions

## Boundaries

- NEVER: Client-side data fetching for initial load
- NEVER: Business logic in components
- NEVER: Skip Zod validation on inputs
- NEVER: Direct Prisma calls outside server/
- ASK FIRST: New Prisma migrations
- ASK FIRST: New auth providers
- ASK FIRST: New API routes (prefer Server Actions)
```

## Variant: T3 Stack

```markdown
# Project

[Description]

## Tech Stack

- Framework: Next.js 14 (App Router)
- Language: TypeScript (strict)
- API: tRPC
- Database: PostgreSQL + Drizzle
- Auth: Lucia
- Styling: Tailwind CSS
- Validation: Zod

## Commands

```bash
pnpm dev          # Start development
pnpm db:push      # Push schema
pnpm db:studio    # Drizzle Studio
pnpm build        # Production build
```

## Structure

```
src/
├── app/                   # Next.js App Router
├── components/            # React components
├── server/
│   ├── api/
│   │   ├── routers/       # tRPC routers
│   │   ├── trpc.ts        # tRPC setup
│   │   └── root.ts        # Root router
│   ├── db/
│   │   ├── schema.ts      # Drizzle schema
│   │   └── index.ts       # DB client
│   └── auth/              # Lucia auth
├── lib/
│   └── trpc.ts            # tRPC client
└── env.js                 # Type-safe env
```

## tRPC Conventions

- Routers in `server/api/routers/`
- Procedures: `publicProcedure`, `protectedProcedure`
- Input validation with Zod in procedure definition
- Client calls via `api.[router].[procedure].useQuery/useMutation`

## Principles

1. End-to-end type safety: tRPC + Drizzle + Zod
2. Server-first: RSC for data, tRPC for mutations
3. Validated environment: Type-safe env with t3-env

## Boundaries

- NEVER: Skip input validation
- NEVER: Use raw fetch for API calls
- ASK FIRST: New tRPC routers
- ASK FIRST: Schema changes
```

## Variant: SvelteKit Full Stack

```markdown
# Project

[Description]

## Tech Stack

- Framework: SvelteKit
- Language: TypeScript
- Database: PostgreSQL
- ORM: Prisma
- Auth: Lucia
- Styling: Tailwind CSS

## Commands

```bash
pnpm dev          # Development
pnpm build        # Build
pnpm preview      # Preview build
pnpm db:push      # Push schema
```

## Structure

```
src/
├── routes/
│   ├── (app)/             # Protected routes
│   ├── (auth)/            # Auth routes
│   ├── api/               # API endpoints
│   └── +layout.svelte     # Root layout
├── lib/
│   ├── components/        # Svelte components
│   ├── server/            # Server-only code
│   │   ├── db.ts
│   │   └── auth.ts
│   └── utils.ts
└── app.d.ts               # Type definitions

prisma/
└── schema.prisma
```

## SvelteKit Conventions

- `+page.server.ts` for server load functions
- `+page.ts` for universal load functions
- Form actions for mutations
- `$lib/server/` for server-only code

## Principles

1. Progressive enhancement: Forms work without JS
2. Server-first: Load data on server
3. Type safety: Strict TypeScript

## Boundaries

- NEVER: Import from `$lib/server/` in client code
- ASK FIRST: New API endpoints
- ASK FIRST: Database schema changes
```
