---
inclusion: manual
---

# Feature Development Guide

## Adding New File Categories

### Steps:
1. Update `config.yaml` with new category and MIME types:
```yaml
categories:
  NewCategory: ['mime/type1', 'mime/type2']
```

2. Test with sample files of that type
3. Verify categorization in dry-run mode
4. Update README.md with new category example

## Adding New Configuration Options

### Steps:
1. Add new key to `config.yaml`
2. Update `load_config()` in `main.py` if validation needed
3. Access config in relevant module via `self.config.get('new_key', default_value)`
4. Document in README.md Configuration section
5. Test with and without the new option

## Extending Duplicate Handling

Current strategies: 'rename', 'skip'

### To Add New Strategy:
1. Add new strategy to `_move_file()` in `organizer.py`
2. Update config.yaml documentation
3. Add validation in config loading
4. Test new strategy behavior

## Adding New Report Metrics

### Steps:
1. Initialize new metric in `report_data` dict in `organizer.py.__init__()`
2. Increment metric in appropriate method
3. Verify metric appears in generated JSON report
4. Document metric meaning in README

## Performance Optimization Ideas

### Current Optimizations:
- ThreadPoolExecutor for parallel file processing
- SHA256 hash caching to avoid recomputation
- Lazy file reading (8KB chunks)

### Potential Improvements:
- Add progress bar for large directories
- Implement file size threshold for parallel processing
- Cache MIME type results for similar files
- Add option to limit concurrent threads

## Code Quality Tools

### Linting:
```bash
flake8 src/
```

### Type Checking (if mypy added):
```bash
mypy src/
```

### Code Formatting (if black added):
```bash
black src/
```
