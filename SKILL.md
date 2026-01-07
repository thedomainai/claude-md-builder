---
name: claude-md-builder
description: Generate optimized CLAUDE.md files for Claude Code projects. Use when user wants to create a new CLAUDE.md, asks how to set up Claude Code, mentions project constitution or project rules, or wants to configure Claude Code behavior. Supports web frontend, backend, fullstack, CLI, library, and monorepo projects.
---

# CLAUDE.md Builder

Generate optimized CLAUDE.md files that serve as the "constitution" for Claude Code projects.

## What is CLAUDE.md?

CLAUDE.md is the single source of truth that governs Claude Code's behavior in a project. Unlike Cursor's `.cursorrules` with glob-based conditional loading, Claude Code reads CLAUDE.md in full at every interaction.

### Key Characteristics

- **Always fully loaded**: No conditional loading - keep it concise
- **Supreme authority**: Overrides all other guidance when conflicts arise
- **Project-specific**: Tailored to each project's unique needs
- **Living document**: Evolves with the project

## CLAUDE.md Structure

A well-structured CLAUDE.md contains these sections:

```
CLAUDE.md
├── Project Identity (WHO)
│   └── What is this project? One-line description.
│
├── Tech Stack (WHAT)
│   └── Languages, frameworks, key dependencies
│
├── Directory Structure (WHERE)
│   └── Key directories and their responsibilities
│
├── Commands (HOW - Operations)
│   └── Frequently used commands (dev, test, build, deploy)
│
├── Principles (HOW - Decisions)
│   └── Priority order for trade-offs (e.g., "Type safety > Brevity")
│
├── Boundaries (WHAT NOT)
│   └── Prohibited actions, approval-required changes
│
└── References (OPTIONAL)
    └── Pointers to detailed docs when needed
```

## Workflow

### Step 1: Gather Context

Ask the user about their project. Key questions:

1. **Project purpose**: "What does this project do in one sentence?"
2. **Tech stack**: "What technologies are you using?" (or detect from package.json/pyproject.toml)
3. **Team context**: "Is this solo or team project? Any specific conventions?"
4. **Pain points**: "What mistakes should Claude avoid?"

If the project already exists, offer to analyze it:
- Check for package.json, pyproject.toml, Cargo.toml, go.mod
- Scan directory structure
- Look for existing documentation

### Step 2: Select Template

Based on context, select the appropriate template from `references/templates/`:

| Project Type | Template | Key Focus |
|-------------|----------|-----------|
| Web Frontend | `web-frontend.md` | Components, state, styling |
| Web Backend | `web-backend.md` | API, DB, auth, security |
| Full Stack | `fullstack.md` | Both + integration points |
| CLI Tool | `cli.md` | Args, UX, error handling |
| Library/SDK | `library.md` | API design, compatibility |
| Monorepo | `monorepo.md` | Workspace, dependencies |
| Minimal | `minimal.md` | Bare essentials only |

### Step 3: Customize Sections

For each section, consult `references/sections/` for detailed guidance:

- `identity.md` - Writing effective project descriptions
- `boundaries.md` - Defining constraints and approval gates
- `context.md` - Technical context best practices
- `workflow.md` - Git and development workflow rules

### Step 4: Generate & Validate

1. Generate CLAUDE.md using the template and customizations
2. Run `scripts/validate_claude_md.py` to check:
   - Required sections present
   - Line count within limits (recommended: <200 lines)
   - No conflicting instructions
3. Present to user for review

### Step 5: Recommend Companion Docs

If the project needs detailed documentation, suggest creating:

```
docs/
├── ARCHITECTURE.md  # System design, boundaries
├── CONVENTIONS.md   # Coding standards
└── API.md           # API documentation
```

CLAUDE.md should reference these with pointers like:
```markdown
## References
- Architecture details: See `docs/ARCHITECTURE.md`
- Coding conventions: See `docs/CONVENTIONS.md`
```

## Design Principles

### 1. Concise > Comprehensive

Claude Code reads CLAUDE.md fully every time. Every line must justify its token cost.

**Bad**: 500-line exhaustive rulebook
**Good**: 100-line focused constitution with doc pointers

### 2. Declarative > Procedural

CLAUDE.md declares WHAT and WHY, not HOW step-by-step.

**Bad**: "First run npm install, then run npm run dev..."
**Good**: "Dev server: `npm run dev`"

### 3. Priorities > Rules

Explicit priority ordering helps Claude make trade-off decisions.

**Bad**: "Write clean code. Write performant code."
**Good**: "Priorities: 1. Correctness 2. Readability 3. Performance"

### 4. Boundaries > Permissions

Define what NOT to do. Claude defaults to being helpful.

**Bad**: "You may create new files in src/"
**Good**: "NEVER modify files in src/generated/"

## Output Guidelines

When generating CLAUDE.md:

1. **Start minimal**: Begin with essential sections, expand only if needed
2. **Use consistent formatting**: Headers, code blocks, lists
3. **Include concrete examples**: Show exact commands, not descriptions
4. **Add comments sparingly**: Only for non-obvious decisions
