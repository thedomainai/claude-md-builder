# Workflow Section Guide

The Workflow section answers: **"How do we develop and ship code?"**

## Purpose

This section codifies development practices, particularly around Git, testing, and code review. It helps Claude follow team conventions and suggest appropriate workflows.

## When to Include

Include a Workflow section when:
- You have specific Git conventions (branch naming, commit format)
- You have a defined PR process
- Testing requirements vary by change type
- Deployment has specific steps or gates

Skip if you're solo and have no strong conventions.

---

## Git Workflow

### Branch Naming

```markdown
## Workflow

### Branches
- `main` - Production, always deployable
- `feature/[ticket]-description` - New features
- `fix/[ticket]-description` - Bug fixes
- `chore/description` - Maintenance, deps
```

### Commit Messages

**Conventional Commits:**
```markdown
### Commits
Follow Conventional Commits:
- `feat(scope): description` - New feature
- `fix(scope): description` - Bug fix
- `docs(scope): description` - Documentation
- `refactor(scope): description` - Code change (no feature/fix)
- `test(scope): description` - Tests only
- `chore(scope): description` - Maintenance

Examples:
```
feat(auth): add password reset flow
fix(api): handle null response from payment gateway
docs(readme): update installation instructions
```
```

**Simple format:**
```markdown
### Commits
Format: `[type] Short description`

Types: feat, fix, docs, refactor, test, chore

Examples:
- `[feat] Add user export functionality`
- `[fix] Prevent duplicate form submissions`
```

---

## Pull Request Process

```markdown
### Pull Requests

1. Create branch from `main`
2. Make changes, commit following conventions
3. Push and open PR with:
   - Clear title (same format as commits)
   - Description of changes
   - Link to ticket/issue
   - Screenshots for UI changes
4. Ensure CI passes
5. Request review from appropriate team member
6. Address feedback, squash if needed
7. Merge when approved (squash merge to main)
```

### PR Size Guidelines

```markdown
### PR Guidelines

- Prefer small, focused PRs (<400 lines changed)
- Split large features into incremental PRs
- One concern per PR (don't mix refactoring with features)
```

---

## Testing Requirements

```markdown
### Testing

- **New features**: Unit tests required, integration tests for complex flows
- **Bug fixes**: Add regression test proving the fix
- **Refactoring**: Ensure existing tests pass
- **UI changes**: Visual review required

Run before pushing:
```bash
pnpm test && pnpm lint && pnpm typecheck
```
```

### Coverage Requirements

```markdown
### Coverage

- Minimum 80% for new code
- Critical paths (auth, payments) require 90%+
- Don't test implementation details
```

---

## Deployment

```markdown
### Deployment

- `main` auto-deploys to staging
- Production deploys require:
  1. All tests passing
  2. Staging verification
  3. Manual trigger in CI

Rollback:
```bash
# Revert and deploy
git revert <commit>
git push origin main
```
```

---

## Example: Complete Workflow Section

```markdown
## Workflow

### Branches
- `main` - Production-ready code
- `feature/[JIRA-XXX]-description` - Features
- `fix/[JIRA-XXX]-description` - Bug fixes
- `hotfix/description` - Urgent production fixes

### Commits
Conventional Commits format:
```
type(scope): description

[optional body]
[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore
Scope: component or area affected (auth, api, ui, etc.)

### Pull Requests
1. Branch from latest `main`
2. Keep PRs focused and <400 lines when possible
3. Include:
   - Descriptive title following commit format
   - Link to JIRA ticket
   - Summary of changes
   - Testing notes
   - Screenshots for UI changes
4. Require 1 approval for features, 2 for core changes
5. Squash merge to main

### Testing
- Unit tests required for new logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Run `pnpm test:all` before pushing

### Deployment
- PRs to main trigger staging deploy
- Production deploy via GitHub release
- Hotfixes can bypass staging with approval
```

---

## Workflow for Claude-Specific Conventions

If you have conventions specific to AI-assisted development:

```markdown
## Workflow

### Working with Claude

When making changes:
1. Explain the change clearly before implementing
2. Show the plan for multi-file changes
3. Run tests after each logical change
4. Commit in logical units (not one giant commit)

For large refactors:
1. Create a plan document first
2. Get approval on approach
3. Implement incrementally with checkpoints
```

---

## Anti-Patterns

### Over-Specified
```markdown
### Commits
1. Open terminal
2. Type `git add .`
3. Type `git commit -m "..."`
4. Type `git push`
```
Claude knows how to use Git.

### Under-Specified
```markdown
### Workflow
Make good commits and PRs.
```
What makes a commit or PR "good" in this project?

### Conflicting Rules
```markdown
- Commit frequently to save work
- Each commit should be a complete, working state
```
These can conflict. Clarify priorities.

---

## Checklist

- [ ] Branch naming convention defined
- [ ] Commit message format specified
- [ ] PR process documented
- [ ] Testing requirements by change type
- [ ] Deployment process noted (if relevant)
- [ ] Not over-explained (Claude knows basics)
- [ ] Specific to this project's needs
- [ ] No conflicting guidance
