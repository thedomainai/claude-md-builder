# Web Frontend CLAUDE.md Template

Use for React, Vue, Svelte, or other frontend projects.

## Template

```markdown
# Project

[One-line description]

## Tech Stack

- Framework: [React/Vue/Svelte/etc.]
- Language: [TypeScript/JavaScript]
- Styling: [Tailwind/CSS Modules/styled-components/etc.]
- State: [Zustand/Redux/Jotai/etc.]
- Build: [Vite/Next.js/etc.]

## Commands

```bash
# Development
[npm run dev / pnpm dev]

# Test
[npm test / pnpm test]

# Build
[npm run build]

# Lint
[npm run lint]

# Type check
[npm run typecheck]
```

## Structure

```
src/
├── components/    # Reusable UI components
│   ├── ui/        # Primitive components (Button, Input)
│   └── features/  # Feature-specific components
├── hooks/         # Custom React hooks
├── lib/           # Utilities, helpers
├── styles/        # Global styles, themes
└── types/         # TypeScript type definitions
```

## Component Guidelines

- Naming: PascalCase for components, camelCase for hooks
- One component per file, co-locate styles and tests
- Props interface named `[Component]Props`
- Prefer composition over prop drilling

## Principles

1. Type safety: Strict TypeScript, no `any`
2. Accessibility: Semantic HTML, ARIA when needed
3. Performance: Lazy load routes, memoize expensive renders
4. Consistency: Follow existing patterns in codebase

## Boundaries

- NEVER: Install new dependencies without discussion
- NEVER: Disable TypeScript strict mode
- NEVER: Use inline styles except for dynamic values
- ASK FIRST: Major state management changes
- ASK FIRST: New routing patterns
```

## Variant: Next.js App Router

```markdown
# Project

[Description]

## Tech Stack

- Framework: Next.js 14+ (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Database: [Prisma/Drizzle + DB]

## Commands

```bash
npm run dev      # Start dev server
npm run build    # Production build
npm run start    # Start production server
npm run lint     # ESLint
npm run db:push  # Push schema changes
```

## Structure

```
app/
├── (auth)/           # Auth route group
├── (dashboard)/      # Dashboard route group
├── api/              # API routes
└── layout.tsx        # Root layout

components/
├── ui/               # shadcn/ui components
└── [feature]/        # Feature components

lib/
├── db.ts             # Database client
├── auth.ts           # Auth utilities
└── utils.ts          # General utilities
```

## Conventions

- Server Components by default
- 'use client' only when needed (interactivity, hooks)
- Data fetching in Server Components
- Server Actions for mutations
- Parallel routes for modals

## Principles

1. Server-first: Maximize Server Components
2. Type safety: End-to-end types with Prisma
3. Performance: Streaming, Suspense boundaries
4. Security: Validate all inputs, sanitize outputs

## Boundaries

- NEVER: Use `use client` without justification
- NEVER: Expose server-only code to client
- NEVER: Skip input validation on API routes
- ASK FIRST: New middleware logic
- ASK FIRST: Database schema changes
```

## Variant: React SPA with Vite

```markdown
# Project

[Description]

## Tech Stack

- Framework: React 18+
- Build: Vite
- Language: TypeScript
- Styling: Tailwind CSS
- State: Zustand
- Routing: React Router v6
- API: TanStack Query

## Commands

```bash
pnpm dev        # Start dev server (port 5173)
pnpm build      # Production build
pnpm preview    # Preview production build
pnpm test       # Run Vitest
pnpm lint       # ESLint + Prettier check
```

## Structure

```
src/
├── components/     # UI components
├── features/       # Feature modules
│   └── [feature]/
│       ├── api.ts        # API calls
│       ├── hooks.ts      # Feature hooks
│       ├── store.ts      # Zustand slice
│       └── components/   # Feature UI
├── hooks/          # Shared hooks
├── lib/            # Utilities
├── routes/         # Route components
└── types/          # Shared types
```

## Conventions

- Feature-based organization
- Colocate related code in feature folders
- Shared components in top-level components/
- API calls wrapped in TanStack Query hooks

## Principles

1. Feature isolation: Features should be self-contained
2. Type safety: Strict mode, no implicit any
3. Testing: Test business logic, not implementation
4. Performance: Code split by route

## Boundaries

- NEVER: Direct API calls outside TanStack Query
- NEVER: Global state for server data (use Query)
- ASK FIRST: New top-level dependencies
- ASK FIRST: Changes to routing structure
```
