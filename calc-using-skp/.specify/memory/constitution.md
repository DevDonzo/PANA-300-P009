<!--
Sync Impact Report
==================
- Version change: 0.0.0 → 1.0.0 (MAJOR: initial constitution)
- Modified principles: N/A (initial creation)
- Added sections:
  - Core Principles (I-V)
  - Code Quality Standards
  - Development Workflow
  - Governance
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (compatible, no changes needed)
  - .specify/templates/spec-template.md ✅ (compatible, no changes needed)
  - .specify/templates/tasks-template.md ✅ (compatible, no changes needed)
- Follow-up TODOs: None
-->

# Python Calculator Constitution

## Core Principles

### I. Type Safety

All code MUST use Python type hints throughout. This is NON-NEGOTIABLE.

- All function parameters MUST have type annotations
- All function return types MUST be annotated
- Complex types MUST use `typing` module constructs (e.g., `Optional`, `Union`, `List`, `Dict`)
- Type hints enable static analysis and improve code maintainability

**Rationale**: Type hints catch errors at development time, serve as inline documentation, and enable IDE autocompletion.

### II. Test-First Development

TDD is mandatory: write tests before implementation.

- Red-Green-Refactor cycle strictly enforced
- Tests MUST fail before implementation begins
- All calculator operations MUST have corresponding unit tests
- Edge cases (division by zero, overflow, invalid input) MUST be tested

**Rationale**: Test-first ensures requirements are understood before coding and prevents regression.

### III. Single Responsibility

Each module and function MUST have one clear purpose.

- Calculator operations separated by function (add, subtract, multiply, divide)
- Input parsing separated from calculation logic
- Output formatting separated from business logic
- No god classes or functions

**Rationale**: Single responsibility makes code easier to test, debug, and maintain.

### IV. Clean Dependencies

Dependencies MUST be managed via pip with explicit version constraints.

- All dependencies declared in `requirements.txt` or `pyproject.toml`
- Development dependencies separated from production dependencies
- Virtual environment usage REQUIRED for isolation
- Pin major versions to prevent breaking changes

**Rationale**: Explicit dependency management ensures reproducible builds across environments.

### V. Simplicity

Start simple and add complexity only when justified.

- YAGNI (You Aren't Gonna Need It) principle applies
- Prefer stdlib over external packages when sufficient
- No premature optimization
- Smallest viable change for each task

**Rationale**: Simple code is easier to understand, test, and maintain.

## Code Quality Standards

### Formatting and Style

- Code MUST follow PEP 8 style guidelines
- Maximum line length: 88 characters (Black formatter default)
- Imports MUST be sorted and grouped (stdlib, third-party, local)
- Docstrings MUST use Google or NumPy style consistently

### Error Handling

- Calculator MUST handle invalid inputs gracefully
- Division by zero MUST raise or return a clear error
- Error messages MUST be user-friendly and actionable
- Never silently swallow exceptions

### Testing Standards

- Minimum test coverage: 90% for calculator logic
- Tests organized in `tests/` directory mirroring `src/` structure
- Test naming: `test_<function>_<scenario>_<expected_result>`
- Use pytest as the testing framework

## Development Workflow

### Branch Strategy

- Feature branches from `main`
- Branch naming: `<type>/<description>` (e.g., `feature/add-division`, `fix/zero-handling`)
- Squash commits on merge to main

### Code Review Requirements

- All changes require review before merge
- Constitution compliance verified in each review
- Tests MUST pass before merge approval

### Commit Standards

- Conventional commits format: `<type>: <description>`
- Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`
- Each commit represents one logical change

## Governance

This constitution supersedes all other project practices. Any deviation MUST be documented and justified in an ADR.

**Amendment Process**:
1. Propose amendment with rationale
2. Document in ADR if architecturally significant
3. Update constitution with version increment
4. Propagate changes to dependent templates

**Versioning Policy**:
- MAJOR: Backward-incompatible principle changes or removals
- MINOR: New principles or material expansions
- PATCH: Clarifications, wording improvements

**Compliance**:
- All PRs MUST verify constitution compliance
- Complexity MUST be justified against simplicity principle
- See `.specify/` for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
