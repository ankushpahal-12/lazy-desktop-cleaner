---
inclusion: manual
---

# Common Development Tasks

## Setup and Installation

### Initial Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Linux-Specific Setup
```bash
# Install libmagic for python-magic
sudo apt-get update && sudo apt-get install -y libmagic1
```

## Running the Application

### Standard Run
```bash
python -m src.uldc.main
```

### Dry-Run (Safe Testing)
```bash
python -m src.uldc.main --dry-run
```

### With Custom Config
```bash
python -m src.uldc.main --config test-config.yaml
```

## Code Quality Checks

### Run Linter
```bash
flake8 src/ --max-line-length=100
```

### Check for Common Issues
- Unused imports
- Undefined variables
- PEP 8 violations
- Complexity warnings

## Debugging Tips

### Enable Verbose Logging
Modify logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

### Test Individual Modules
```python
# Test categorizer
from src.uldc.categorizer import FileCategorizer
categorizer = FileCategorizer({'Images': ['image/jpeg']})
print(categorizer.categorize(Path('test.jpg')))

# Test hashing
from src.uldc.hashing import get_file_hash
print(get_file_hash(Path('test.txt')))
```

### Common Debug Scenarios
1. **Files not categorizing correctly**: Check MIME type detection
2. **Duplicates not detected**: Verify hash computation
3. **Files not moving**: Check permissions and dry-run mode
4. **Config errors**: Validate YAML syntax

## Updating Dependencies

### Check for Updates
```bash
pip list --outdated
```

### Update Specific Package
```bash
pip install --upgrade PyYAML
```

### Regenerate requirements.txt
```bash
pip freeze > requirements.txt
```

## Git Workflow

### Before Committing
1. Run linter: `flake8 src/`
2. Test in dry-run mode
3. Verify no sensitive data in config files
4. Update README if features changed

### Commit Message Format
```
type: brief description

- Detailed change 1
- Detailed change 2

Types: feat, fix, docs, refactor, test, chore
```
