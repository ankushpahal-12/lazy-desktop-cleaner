---
inclusion: always
---

# Coding Standards for Lazy Desktop Cleaner

## Python Style Guide
- Follow PEP 8 conventions
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable and function names

## Type Hints
- Always include type hints for function parameters and return values
- Use `typing` module for complex types (Dict, List, Any, Optional)
- Example: `def process_file(file_path: Path, dry_run: bool) -> None:`

## Error Handling
- Use try-except blocks for I/O operations
- Log errors with appropriate severity levels (ERROR, WARNING, CRITICAL)
- Include `exc_info=True` for critical errors to capture stack traces
- Gracefully handle missing dependencies (e.g., python-magic fallback)

## Logging Best Practices
- Use the `logging` module, not print statements
- Log levels:
  - INFO: Normal operations (file moves, processing)
  - WARNING: Duplicates found, fallback behavior
  - ERROR: Recoverable errors (file access issues)
  - CRITICAL: Fatal errors that halt execution
- Include context in log messages (file names, paths, actions)

## Concurrency
- Use `ThreadPoolExecutor` for I/O-bound operations
- Handle exceptions within thread workers
- Use `as_completed()` for processing results as they finish

## Path Handling
- Always use `pathlib.Path` instead of string concatenation
- Use `.expanduser()` for paths with `~`
- Use `.resolve()` for absolute paths when needed
- Check file existence before operations

## Testing Considerations
- Support dry-run mode for all file operations
- Validate configuration before processing
- Create parent directories with `mkdir(exist_ok=True, parents=True)`
