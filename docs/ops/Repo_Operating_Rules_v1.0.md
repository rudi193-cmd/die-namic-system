# Repo Operating Rules

**Version:** v1.0  
**Date:** 2025-12-15  
**Repository:** die-namic-system

---

## Branch Strategy

### Protected Branch

- `main` — Production-ready code only
- Direct push: **Disabled** (PR required)
- Merge requires: 1 approval minimum

### Feature Branches

```
v{version}/{description}

Examples:
  v23.3/dual-license
  v23.4/docs-update
  v24.0/lattice-refactor
```

### Naming Conventions

- Lowercase
- Hyphens for spaces
- Version prefix required for release-track work
- Descriptive but concise

---

## Commit Conventions

### Format

```
{type}: {short description}

{optional body}

{optional footer}
```

### Types

| Type | Use Case |
|------|----------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `chore` | Maintenance, dependencies |
| `refactor` | Code restructure, no behavior change |
| `test` | Adding or updating tests |
| `style` | Formatting, no code change |

### Examples

```
feat: add ΔE calculation module
docs: update AWA routing rules
chore: add MIT and CC BY-NC licenses
fix: correct lattice neighbor lookup
```

---

## PR Requirements

### Title Format

```
v{version}: {short description}
```

### Description Must Include

1. **Summary** — 2-5 bullets describing changes
2. **Files Changed** — Key files (auto-populated by template)
3. **Licensing Impact** — Yes/No + explanation if yes
4. **Blockers/Follow-ups** — Future work enabled

### Review Checklist

- [ ] Code follows project style
- [ ] Documentation updated (if applicable)
- [ ] No new warnings or errors
- [ ] Tested locally
- [ ] Licensing correctly attributed

---

## Review Process

### Standard Flow

1. Create feature branch
2. Make changes
3. Open PR with template
4. Request review
5. Address feedback
6. Merge when approved

### Fast-Track (Documentation Only)

- Docs-only PRs may self-merge after 24h if no objections
- Still requires PR (no direct push)

### Emergency Hotfix

- Prefix branch: `hotfix/`
- May merge with single approval
- Requires post-merge review within 48h

---

## File Organization

### Root Level

```
/
├── LICENSE, LICENSE-MIT, LICENSE-CC-BY-NC
├── NOTICE.md
├── README.md
├── CHANGELOG.md
├── package.json
└── .github/
```

### Documentation

```
/docs/
├── awa/           # Workflow architecture
├── whitepapers/   # Technical papers
├── ops/           # Operating procedures
└── policies/      # Behavioral policies
```

### Core System

```
/source_ring/      # Technical modules
/bridge_ring/      # Human interface layer
/continuity_ring/  # Archives & seals
/infrastructure/   # Build & deploy
/governance/       # System governance
```

---

## Code Style

### JavaScript/TypeScript

- 2-space indentation
- Single quotes
- No semicolons (unless required)
- ES6+ syntax

### Python

- 4-space indentation
- PEP 8 compliance
- Type hints encouraged
- Docstrings required for public functions

### Markdown

- ATX headers (`#`, `##`, `###`)
- Blank line before/after code blocks
- Fenced code blocks with language tags

---

## Related Documents

- `/docs/ops/Release_Process_v0.1.md`
- `/.github/PULL_REQUEST_TEMPLATE.md`
- `/.github/CODEOWNERS`

---

*Consistency enables velocity.*
