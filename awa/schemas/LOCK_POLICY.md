# AWA Schema Lock Policy

## Purpose
Establish immutable, versioned schemas for AWA artifacts to guarantee:
- Machine-validatable artifacts
- Enforceable lineage
- Stable contracts for implementation and CI gates
- Fail-closed behavior against drift and undeclared context

## Immutability
All files under `/awa/schemas/vX.Y.Z/` are **immutable** once published.

- Do **not** modify schemas in a locked folder.
- Changes must be published as a new version folder.
- Prior versions remain available for historical validation.

## Versioning (SemVer)
Schemas are versioned using `MAJOR.MINOR.PATCH`.

### MAJOR
Breaking change:
- required fields added/removed
- field type changes
- enum restrictions tightened
- additionalProperties behavior altered
- identifier semantics changed

### MINOR
Backward-compatible change:
- optional fields added
- new enum values added where they do not invalidate prior valid artifacts

### PATCH
Non-functional change:
- wording clarifications
- description/example edits
- formatting changes that do not affect validation

## Fail-Closed Requirement
Artifact schemas must enforce:
- `additionalProperties: false`
- explicit required fields
- strict enums for key control fields (scope, status, operator, transform_type)

## Publication Workflow
1. Create a new folder `/awa/schemas/vX.Y.Z/`
2. Copy prior schemas forward and apply changes
3. Update `/awa/schemas/SCHEMA_REGISTRY.md` to point to the new current version
4. Add migration notes using `MIGRATION_NOTES_TEMPLATE.md`
5. Do not delete or rewrite previous versions
