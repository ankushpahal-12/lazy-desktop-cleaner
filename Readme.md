# Lazy Desktop Cleaner

> "I hate spending 10 minutes every morning sorting my Desktop — so I built a script that automatically organizes and renames everything for me."

This project is a simple yet powerful Python script that automates the boring, repetitive task of cleaning up a messy directory (like your Desktop!). It scans a folder, categorizes files based on their type, and moves them into neatly organized subfolders.

![CI Badge](https://github.com/ankus/lazy-desktop-cleaner/actions/workflows/ci.yml/badge.svg)

## Features
 
*   **MIME-Based Categorization**: Accurately detects file types using their content (MIME types), not just extensions. Fallback to extension-based categorization is available if `python-magic` is not installed.
*   **True Duplicate Detection**: Uses SHA256 hashing to identify files with identical content, regardless of their filenames.
*   **Parallel Processing**: Employs a `ThreadPoolExecutor` to process multiple files concurrently, dramatically speeding up the cleaning of directories with thousands of files.
*   **Automated Duplicate Handling**: Automatically moves true duplicate files to a dedicated `Duplicates/` folder to prevent clutter.
*   **Archive Old Files**: Compresses and archives files older than a configurable number of days (e.g., 90 days) into a separate `Archived/` directory.
*   **Comprehensive Logging**: Logs all operations to both the console and a file (`organizer.log` by default) for easy review and debugging.
*   **JSON Report Generation**: Creates a detailed JSON report after each run, summarizing all actions taken, including files moved, duplicates found, and archives created.
*   **Safe Dry-Run Mode**: Preview all proposed file movements with the `--dry-run` flag to see what will happen before any changes are made.
*   **Highly Customizable**: Use a simple `config.yaml` file to define which directory to clean, how to handle duplicates, and your own category-to-extension mappings.
*   **CI Integrated**: Includes a GitHub Actions workflow to ensure code quality and linting with `flake8`.

## Installation
 
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/lazy-desktop-cleaner.git
    cd lazy-desktop-cleaner
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    > **Note for Linux Users**: The `python-magic` library requires `libmagic`. You can install it on Debian/Ubuntu systems with:
    > ```bash
    > sudo apt-get update && sudo apt-get install -y libmagic1
    > ```

## How to Run

1.  **Configure the application**:
    Before running, you must create a `config.yaml` file in the project's root directory. This file tells the cleaner which directory to organize and how to categorize the files. See the **Configuration** section below for an example.

2.  **Run the script**:
    Execute the script from the root directory of the project using the following command:
    ```bash
    python -m src.uldc.main
    ```

### Command-Line Arguments

You can customize the script's behavior with this optional argument:

*   `--dry-run`: Run the script in simulation mode. It will print what actions it *would* take without moving any files. This is great for testing your configuration.
    ```bash
    python -m src.uldc.main --dry-run
    ```

## Configuration

Create a `config.yaml` file in the root of the project. Here is an example covering all the new features.

```yaml
# The main folder to scan and organize. Use '~' for the home directory.
source_directory: '~/Desktop'

# Strategy for handling filename conflicts (when a file with the same name
# already exists in the destination folder): 'rename' or 'skip'.
# Note: This does not apply to true duplicates (identical content).
duplicate_strategy: 'rename'

# --- New Features ---

# Directory to move true duplicate files (identified by hash).
duplicates_directory: '~/Desktop/Duplicates'

# Path for the log file.
log_file: '~/Desktop/organizer.log'

# Configuration for archiving old files.
archive_old_files:
  enabled: true
  older_than_days: 90 # Files older than 90 days will be archived.
  archive_folder: '~/Desktop/Archived'

# Mapping of category folders to their corresponding MIME types.
# You can use wildcards, e.g., 'image/*' to catch all image types.
categories:
  Images: ['image/jpeg', 'image/png', 'image/gif', 'image/heic']
  Documents: ['application/pdf', 'application/msword', 'text/plain', 'text/csv']
  Archives: ['application/zip', 'application/x-rar-compressed', 'application/gzip']
  Audio: ['audio/*']
  Video: ['video/*']
```

## Development with Kiro

This project was developed with the assistance of Kiro, a conversational AI code assistant. Kiro helped bootstrap the project, write the core logic, and fix issues, significantly accelerating the development process. The `.kiro` directory in this repository contains artifacts related to the development with Kiro.