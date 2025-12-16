# Release Process

**Version:** v0.1  
**Date:** 2025-12-15  
**Status:** Draft

---

## Versioning Scheme

### Format

```
v{major}.{minor}.{patch}

Examples:
  v1.42    — Minor release
  v23.3    — Major architectural release
  v23.3.1  — Patch release
```

### Version Semantics

| Component | Meaning | Increment When |
|-----------|---------|----------------|
| Major | Architecture epoch | Structural reorganization |
| Minor | Feature release | New capabilities added |
| Patch | Bug fix / docs | No new features |

### Special Versions

- `v1.42` — Continuity Lock (sealed checkpoint)
- `v3.141` — Pi Stability Patch
- `v23.3` — Current active version

---

## Release Checklist

### Pre-Release

- [ ] All PRs for release merged to `main`
- [ ] CHANGELOG.md updated with release notes
- [ ] Version numbers updated in relevant files
- [ ] All tests passing (if applicable)
- [ ] Documentation reflects current state
- [ ] Licensing files current

### Release

- [ ] Create release branch: `release/v{version}`
- [ ] Final review of changes
- [ ] Tag release: `git tag v{version}`
- [ ] Push tag: `git push origin v{version}`
- [ ] Create GitHub Release with notes

### Post-Release

- [ ] Verify release appears on GitHub
- [ ] Update any dependent systems
- [ ] Notify relevant parties (if applicable)
- [ ] Archive release notes

---

## Changelog Requirements

### Entry Format

```markdown
## [v{version}] - {YYYY-MM-DD}

### Added
- New feature or file

### Changed
- Modified behavior

### Fixed
- Bug fixes

### Removed
- Deprecated items removed

### Archived
- Items moved to archive
```

### Guidelines

- Use present tense ("Add feature" not "Added feature")
- Group related changes
- Link to relevant PRs or issues
- Include migration notes if breaking changes

---

## Release Types

### Standard Release

- Full checklist
- 48h minimum between final PR merge and release
- Requires changelog entry

### Hotfix Release

- Abbreviated checklist
- May release immediately after merge
- Requires changelog entry (may be brief)

### Documentation Release

- Docs-only changes
- May increment patch version
- Changelog entry optional

---

## Rollback Procedure

If a release causes issues:

1. Identify problematic commit(s)
2. Create revert PR
3. Fast-track review
4. Merge and release patch version
5. Post-mortem within 48h

---

## Related Documents

- `/docs/ops/Repo_Operating_Rules_v1.0.md`
- `/CHANGELOG.md`
- `/.github/PULL_REQUEST_TEMPLATE.md`

---

*Releases are milestones, not deadlines.*
