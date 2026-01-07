# Boundaries Section Guide

The Boundaries section answers: **"What should Claude NOT do, or do only with approval?"**

## Purpose

Claude defaults to being helpful. Boundaries define constraints to prevent well-intentioned but problematic actions. This section is your guardrail.

## Structure

```markdown
## Boundaries

- NEVER: [Absolute prohibition]
- NEVER: [Another prohibition]
- ASK FIRST: [Action requiring human approval]
- ASK FIRST: [Another approval-required action]
```

## Categories of Boundaries

### 1. Destructive Operations

Actions that can cause data loss or are hard to reverse.

```markdown
- NEVER: Delete files in production directories
- NEVER: Drop database tables
- NEVER: Force push to main branch
- ASK FIRST: Database migrations
- ASK FIRST: Bulk delete operations
```

### 2. Security-Sensitive Areas

Actions that could introduce vulnerabilities.

```markdown
- NEVER: Disable authentication checks
- NEVER: Log sensitive data (passwords, tokens, PII)
- NEVER: Commit secrets to repository
- ASK FIRST: Changes to auth flow
- ASK FIRST: New external API integrations
```

### 3. Architecture Decisions

Changes that affect system structure.

```markdown
- NEVER: Add new top-level directories without discussion
- ASK FIRST: New database tables
- ASK FIRST: New external dependencies
- ASK FIRST: Changes to API contracts
```

### 4. Generated/Protected Files

Files that shouldn't be manually edited.

```markdown
- NEVER: Edit files in src/generated/
- NEVER: Modify lock files directly
- NEVER: Edit .github/workflows/ without review
```

### 5. Code Quality Thresholds

Standards that must be maintained.

```markdown
- NEVER: Disable TypeScript strict mode
- NEVER: Use `any` type without explicit comment
- NEVER: Skip tests for business logic
- NEVER: Commit code with linting errors
```

## NEVER vs ASK FIRST

### Use NEVER When:
- The action is always wrong in this project
- Recovery is difficult or impossible
- Security would be compromised
- It violates non-negotiable standards

### Use ASK FIRST When:
- The action might be valid with context
- Human judgment adds value
- Multiple stakeholders affected
- Reversal is possible but costly

## Examples by Risk Level

### High Risk (NEVER)
```markdown
- NEVER: Expose internal APIs publicly
- NEVER: Store passwords in plain text
- NEVER: Disable rate limiting
```

### Medium Risk (ASK FIRST)
```markdown
- ASK FIRST: New npm dependencies
- ASK FIRST: Changes to CI/CD pipeline
- ASK FIRST: Modifying shared utilities
```

### Context-Specific
```markdown
# For a fintech project
- NEVER: Log transaction amounts
- NEVER: Skip audit trail for money movement
- ASK FIRST: Changes to payment flow

# For a healthcare project
- NEVER: Log patient identifiers
- NEVER: Skip encryption for health data
- ASK FIRST: Changes to consent flow
```

## Anti-Patterns

### Too Restrictive
```markdown
- NEVER: Create new files
- NEVER: Install packages
- ASK FIRST: Any change
```
This makes Claude useless.

### Too Vague
```markdown
- NEVER: Do bad things
- ASK FIRST: Important stuff
```
Claude can't interpret this.

### Missing Critical Boundaries
```markdown
## Boundaries
- NEVER: Use tabs instead of spaces
```
Tabs vs spaces isn't worth a boundary. Database destruction is.

### Duplicating Defaults
```markdown
- NEVER: Write insecure code
- NEVER: Introduce bugs
```
Claude already tries not to do these. Specify what "insecure" means in YOUR context.

## Template by Project Type

### SaaS Application
```markdown
## Boundaries

- NEVER: Expose user data in logs
- NEVER: Skip input validation
- NEVER: Modify subscription/billing code without review
- ASK FIRST: Database schema changes
- ASK FIRST: New third-party integrations
- ASK FIRST: Changes to user-facing error messages
```

### Open Source Library
```markdown
## Boundaries

- NEVER: Break backward compatibility without major version
- NEVER: Add runtime dependencies
- NEVER: Change public API signatures
- ASK FIRST: New exports
- ASK FIRST: New peer dependencies
- ASK FIRST: Deprecation of existing features
```

### Internal Tool
```markdown
## Boundaries

- NEVER: Hardcode credentials
- NEVER: Skip error handling
- ASK FIRST: Changes to data sources
- ASK FIRST: New admin capabilities
```

## Checklist

- [ ] Covers destructive operations
- [ ] Covers security-sensitive areas
- [ ] Covers architecture decisions
- [ ] Specifies protected files/directories
- [ ] Uses NEVER for absolute prohibitions
- [ ] Uses ASK FIRST for context-dependent decisions
- [ ] Not overly restrictive (Claude can still be useful)
- [ ] Not redundant with Claude's defaults
- [ ] Specific to this project's risks
