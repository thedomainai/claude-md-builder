# Identity Section Guide

The Identity section answers: **"What is this project?"**

## Purpose

This section gives Claude immediate context about what it's working on. A clear identity prevents Claude from making assumptions that conflict with the project's nature.

## Structure

```markdown
# Project

[One-line description that captures the essence]
```

## Writing Guidelines

### Be Specific, Not Generic

**Bad:**
```markdown
# Project
A web application.
```

**Good:**
```markdown
# Project
B2B invoicing SaaS for small accounting firms.
```

**Why:** The specific version tells Claude about the domain (B2B, invoicing), the model (SaaS), and the target user (small accounting firms). This influences every decision.

### Include Key Differentiators

If your project has a unique approach, mention it:

```markdown
# Project
Real-time collaborative whiteboard with local-first architecture and CRDT sync.
```

This tells Claude:
- Real-time features are core
- Offline capability matters
- Data sync uses CRDTs (specific technology choice)

### Include Stage if Relevant

```markdown
# Project
E-commerce platform for handmade goods (MVP stage, launching in 2 months).
```

Stage affects decisions:
- MVP: Ship fast, accept tech debt
- Growth: Scalability matters
- Mature: Stability over features

## Examples by Project Type

### SaaS Product
```markdown
# Project
Team wiki with AI-powered search and automatic linking.
```

### Internal Tool
```markdown
# Project
Internal dashboard for monitoring ETL pipeline health across 50+ data sources.
```

### Open Source Library
```markdown
# Project
Zero-dependency TypeScript validation library with 1:1 JSON Schema compatibility.
```

### CLI Tool
```markdown
# Project
Git commit message generator using local LLMs, privacy-focused, no cloud.
```

### API Service
```markdown
# Project
REST API for geocoding with fallback to multiple providers and intelligent caching.
```

## Anti-Patterns

### Too Vague
```markdown
# Project
A project.
```
Claude has no context.

### Too Long
```markdown
# Project
This is a comprehensive enterprise-grade solution for managing customer relationships, 
including contact management, deal tracking, email integration, reporting and analytics,
with support for multiple teams, custom fields, workflows, and API integrations...
```
Save details for other sections.

### Technology-First
```markdown
# Project
Next.js 14 app with Prisma, PostgreSQL, and Redis.
```
This describes HOW, not WHAT. Put tech in the Tech Stack section.

## Checklist

- [ ] One line (two at most)
- [ ] Describes what, not how
- [ ] Includes domain/industry if relevant
- [ ] Includes target user if B2B/B2C
- [ ] Mentions stage if it affects decisions
- [ ] A new team member would understand the project's purpose
