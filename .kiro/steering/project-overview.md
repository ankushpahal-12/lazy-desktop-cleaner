---
inclusion: always
---

# Lazy Desktop Cleaner - Project Overview

## Project Purpose
An automated Python-based desktop file organizer that categorizes, deduplicates, and archives files using MIME type detection and SHA256 hashing.

## Core Architecture

### Module Structure
- `main.py` - Entry point, CLI argument parsing, configuration loading
- `categorizer.py` - MIME-based file categorization with extension fallback
- `organizer.py` - Core orchestration with parallel processing
- `hashing.py` - SHA256 file hashing and unique filename generation
- `reporting.py` - JSON report generation
- `config.py` - Configuration validation and loading utilities

### Key Features
1. **MIME-Based Categorization**: Uses python-magic for accurate file type detection
2. **Duplicate Detection**: SHA256 hashing to identify identical files
3. **Parallel Processing**: ThreadPoolExecutor for concurrent file processing
4. **Archive Old Files**: Compresses files older than configurable threshold
5. **Dry-Run Mode**: Safe preview mode before making changes
6. **Comprehensive Logging**: File and console logging
7. **JSON Reports**: Detailed operation summaries

## Configuration
- Uses `config.yaml` for all settings
- Supports custom category mappings
- Configurable duplicate handling strategies: 'rename' or 'skip'
- Archive settings with age threshold

## Dependencies
- PyYAML==6.0.1
- python-magic (optional, falls back to extension-based categorization)

## Development Guidelines
- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Comprehensive error handling with logging
- Thread-safe operations for parallel processing
