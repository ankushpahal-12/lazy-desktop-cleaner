---
inclusion: manual
---

# Testing Guide for Lazy Desktop Cleaner

## Running the Application

### Basic Usage
```bash
# Activate virtual environment first
python -m src.uldc.main
```

### Dry-Run Mode (Recommended for Testing)
```bash
python -m src.uldc.main --dry-run
```

### Custom Config File
```bash
python -m src.uldc.main --config path/to/custom-config.yaml
```

## Manual Testing Checklist

### 1. Configuration Testing
- [ ] Valid config.yaml loads successfully
- [ ] Missing config.yaml shows appropriate error
- [ ] Invalid YAML syntax is caught and logged
- [ ] Missing required keys (source_directory, categories) are detected

### 2. File Categorization
- [ ] Images are categorized correctly (JPEG, PNG, GIF, HEIC)
- [ ] Documents are categorized correctly (PDF, DOCX, TXT, CSV)
- [ ] Archives are categorized correctly (ZIP, RAR, 7Z, GZIP)
- [ ] Audio/Video files are categorized with wildcards
- [ ] Unknown file types go to "Other" category

### 3. Duplicate Detection
- [ ] Identical files (same content) are detected
- [ ] Duplicates are moved to Duplicates folder
- [ ] Files with same name but different content are not flagged

### 4. Archive Functionality
- [ ] Files older than threshold are archived
- [ ] Archive folder is created if it doesn't exist
- [ ] Original files are deleted after archiving
- [ ] Archives are named correctly

### 5. Conflict Handling
- [ ] 'rename' strategy appends numbers to duplicate filenames
- [ ] 'skip' strategy leaves existing files untouched
- [ ] Unique filename generation works correctly

### 6. Logging and Reporting
- [ ] Log file is created at specified location
- [ ] Console output shows progress
- [ ] JSON report is generated with correct summary
- [ ] Report includes all actions taken

### 7. Dry-Run Mode
- [ ] No files are actually moved in dry-run
- [ ] All proposed actions are logged
- [ ] Report is still generated

## Common Issues and Solutions

### python-magic Not Available
- Application should fall back to extension-based categorization
- Warning should be logged
- Functionality should continue

### Permission Errors
- Check file/folder permissions
- Ensure source directory is accessible
- Verify write permissions for destination folders

### Performance Testing
- Test with large directories (1000+ files)
- Monitor memory usage with many duplicates
- Verify parallel processing improves speed

