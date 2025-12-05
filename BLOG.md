# How I Built a Python Desktop Organizer in Minutes with an AI Assistant

I have a problem: my desktop is a mess. Every day, it gets cluttered with screenshots, downloads, documents, and random files. And every few days, I have to spend 10-15 minutes manually sorting everything into folders. It's a tedious, boring task that I dread.

I'm a developer, so the obvious solution is to automate it. I decided to build a simple Python script to do the job for me. My goal was to create a tool that could:

1.  Scan my desktop directory.
2.  Categorize each file based on its extension (e.g., `.png` -> Images, `.pdf` -> Documents).
3.  Move the files into corresponding folders.
4.  Handle cases where a file with the same name already exists.
5.  Be configurable, so I can easily change the folders and file types.

## Enter Kiro: My AI Code Assistant

I had a clear idea of what I wanted, but I didn't want to spend a whole day writing boilerplate code, looking up file system APIs, and debugging. This is where Kiro, my AI code assistant, came in. I treated it like a pair programmer.

I started with a simple prompt: "I want to build a python script that organizes files on my desktop."

Kiro immediately helped me structure the project. It suggested a `src` directory for the code, a `config.yaml` for configuration, and a `main.py` to run the application.

### Bootstrapping the Code

Kiro generated the initial `main.py` file, which laid out the argument parsing and the main application logic.

```python
# src/uldc/main.py
import argparse
import logging
from pathlib import Path

# ... (imports for config, categorizer, organizer)

def main():
    """Main function to configure and run the desktop cleaner."""
    parser = argparse.ArgumentParser(description="Automatically organize files in a directory.")
    # ... (argument parsing)
    args = parser.parse_args()

    try:
        # Load configuration
        app_config = config.load_config()
        extension_mappings = config.get_category_mappings(app_config)

        # Initialize components
        categorizer = FileCategorizer(extension_mappings)
        organizer = DesktopOrganizer(source_directory, categorizer, duplicate_strategy)

        # Run the cleaner
        organizer.clean(dry_run=args.dry_run)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == '__main__':
    main()
```

This was a great starting point. It established a clean separation of concerns: configuration, categorization, and organization.

### Fixing a "Missing Module" Error

At one point, I had an `ImportError` because the `organizer` module was missing. I wasn't sure where the code went. I asked Kiro "Import .organizer could not be resolved".

Kiro analyzed the codebase, realized the file was missing, and generated the entire `DesktopOrganizer` class for me based on how it was used in `main.py`.

```python
# src/uldc/organizer.py
import logging
import shutil
from pathlib import Path
from .categorizer import FileCategorizer
from .hashing import get_unique_filename

class DesktopOrganizer:
    """Orchestrates the file cleaning process."""

    def __init__(self, source_dir: Path, categorizer: FileCategorizer, duplicate_strategy: str = 'skip'):
        # ...
        pass

    def clean(self, dry_run: bool = False):
        # ...
        for item in self.source_dir.iterdir():
            if item.is_dir():
                continue

            category = self.categorizer.categorize(item)
            destination_dir = self.source_dir / category

            # ... (logic for moving and handling duplicates)
```

This was a huge time saver. I didn't have to write any of this logic myself. Kiro understood the context from the other files and generated a class that fit perfectly.

## Leveling Up: Adding Advanced Features

The basic organizer was great, but I knew it could be better. My desktop doesn't just have filename conflicts; it has *real* duplicates—the same screenshot saved three times with different names. And cleaning a desktop with thousands of files was still slow.

I went back to my AI pair programmer with a new list of demands:

1.  **Detect real duplicates** using file content (hashing), not just filenames.
2.  **Use MIME types** for more accurate categorization instead of just file extensions.
3.  **Process files in parallel** to make it faster.
4.  **Log everything to a file** for a persistent record.
5.  **Generate a JSON report** summarizing the cleanup.
6.  **Archive very old files** automatically.

I prompted Kiro: "Add MIME Detection, Duplicate Detection Using Hashing, Parallel Processing, and Report Generation to the script."

This was a much more complex request, but Kiro handled it brilliantly. It refactored the entire application, breaking the logic into new, focused modules:

*   `hashing.py`: A module for calculating file hashes (SHA256) to find true duplicates.
*   `categorizer.py`: Updated to use the `python-magic` library for MIME-type detection, with a graceful fallback to extensions if the library isn't available.
*   `organizer.py`: The core class was supercharged. Kiro integrated a `ThreadPoolExecutor` for parallel processing and added the logic to use the new hashing and categorizing functions. It also added methods for archiving old files.
*   `reporting.py`: A new module dedicated to generating a clean JSON summary of the entire operation.

The AI even updated the `config.yaml` to include sections for all the new features.

### The Final Result: A Powerful, Efficient Tool

In a remarkably short time, my simple script evolved into a powerful, multi-featured utility. It's now incredibly fast, intelligent, and provides detailed feedback on its work.

Here is a look at the new, more powerful `config.yaml`:

```yaml
# The main folder to scan and organize. Use '~' for the home directory.
source_directory: '~/Desktop'

# Strategy for handling filename conflicts when a file with the same name
# already exists in the destination folder: 'rename' or 'skip'.
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

## Documenting the Collaboration

To make the process transparent, I decided to document my interactions with the AI. I created a `.kiro` directory in the repository to serve as a logbook for our collaboration.

Inside, the `recording-notes.md` file contains a log of my key prompts and the AI's responses. This includes everything from the initial feature request to debugging dependency issues. It serves as direct proof of how AI assistance accelerated the project, turning high-level ideas into functional code.

## Conclusion

Working with an AI assistant like Kiro was a game-changer for this project. It took care of the tedious parts of coding, allowing me to focus on the high-level logic and design. What might have taken me a few hours to build from scratch, I was able to complete in a matter of minutes.

This experience has shown me that AI assistants are not just for answering simple questions; they can be powerful partners in the development process, helping to accelerate development and reduce boilerplate.

By documenting the journey in the `.kiro` directory, I've created a transparent record of how a developer and an AI can work together to build something cool, fast.
