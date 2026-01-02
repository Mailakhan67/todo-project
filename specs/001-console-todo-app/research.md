# Research: In-Memory Python Console Todo App

## Technical Stack Decisions

### Language: Python 3.10+

**Decision**: Use Python 3.10+ with only standard library dependencies.

**Rationale**:
- Python's stdlib includes everything needed: `argparse` for CLI, `dataclasses` for models, `datetime` for timestamps
- No external dependencies means easier setup, no pip install issues, portable across environments
- Python is specified in the constitution and project context

**Alternatives Considered**:
- Python with Click/Typer: Adds dependency for nicer CLI, but stdlib `argparse` is sufficient
- Python with SQLAlchemy: Overkill for in-memory storage per Phase I requirements

---

### CLI Framework: argparse (stdlib)

**Decision**: Use `argparse` for command-line interface.

**Rationale**:
- Built into Python stdlib, zero dependencies
- Supports subcommands (add, view, update, delete, complete) cleanly
- Handles argument validation and help generation

**Alternatives Considered**:
- Click: Popular third-party CLI framework, more ergonomic but adds dependency
- Manual input(): Simpler but less robust; argparse provides better UX with help/error messages

---

### Data Model: dataclasses

**Decision**: Use Python `dataclass` for Task entity.

**Rationale**:
- Clean, declarative syntax for defining data structures
- Built-in `__eq__`, `__repr__`, field defaults
- Type hints integrate well with IDEs and mypy if needed later

**Alternatives Considered**:
- Pydantic: Powerful validation but adds dependency, overkill for this scope
- Named tuple: Less flexible, immutable (need mutability for updates)
- Plain dict: No type safety, less self-documenting

---

### Testing: pytest

**Decision**: Use pytest for testing.

**Rationale**:
- Standard Python testing framework
- Fixtures for test setup, parametrize for multiple test cases
- Clear failure output with detailed tracebacks

**Alternatives Considered**:
- unittest: Built-in but more verbose, pytest is more ergonomic
- doctest: Good for simple examples but insufficient for comprehensive test suite

---

### Storage: In-Memory List

**Decision**: Use Python list with dictionary index for O(1) lookups by ID.

**Rationale**:
- Per constitution Phase I requirements: "todos stored in Python in-memory data structure"
- Simple list + dict provides:
  - O(1) insertion
  - O(1) lookup by ID (dict index)
  - O(n) iteration for viewing all (acceptable for small lists)

**Alternatives Considered**:
- List only: O(n) lookup by ID, acceptable but dict is cleaner
- Sorted list: Over-engineering for current scale

---

## Best Practices References

1. **CLI Design**: Follow Unix conventions (subcommands, --help flag, exit codes)
2. **Error Handling**: Use specific exception types, provide actionable messages
3. **Testing**: Arrange-Act-Assert pattern, test edge cases (empty input, invalid IDs)

---

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Export/import feature? | Marked optional in spec, defer to Phase II if needed |
| Task ID generation? | Auto-incrementing integer starting from 1 |
| How to handle concurrent modifications? | Single-user context, no locking needed |
| Max task title length? | No hard limit; rely on practical terminal width |
