import logging
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from .categorizer import FileCategorizer
from .hashing import get_file_hash, get_unique_filename


class DesktopOrganizer:
    """Orchestrates the file cleaning process with advanced features."""

    def __init__(self, source_dir: Path, categorizer: FileCategorizer, config: Dict[str, Any]):
        self.source_dir = source_dir
        self.categorizer = categorizer
        self.config = config
        self.duplicate_strategy = config.get('duplicate_strategy', 'skip')
        self.duplicates_dir = Path(config.get('duplicates_directory', '~/Desktop/Duplicates')).expanduser()
        self.archive_config = config.get('archive_old_files', {})
        self.hash_cache: Dict[str, Path] = {}
        self.report_data: Dict[str, Any] = {
            "summary": {"files_scanned": 0, "files_moved": 0, "duplicates_found": 0, "archives_created": 0},
            "actions": []
        }

    def _process_file(self, item: Path, dry_run: bool) -> None:
        """Processes a single file: categorizes, checks for duplicates, and moves it."""
        if item.is_dir() or not item.is_file():
            return

        self.report_data["summary"]["files_scanned"] += 1
        logging.info(f"Processing: {item.name}")

        # 1. Duplicate detection
        file_hash = get_file_hash(item)
        if file_hash and file_hash in self.hash_cache:
            logging.warning(f"Duplicate found: {item.name} is identical to {self.hash_cache[file_hash].name}")
            self._handle_duplicate(item, dry_run)
            return
        if file_hash:
            self.hash_cache[file_hash] = item

        # 2. Archive old files
        if self._archive_old_file(item, dry_run):
            return

        # 3. Categorize and move
        category = self.categorizer.categorize(item)
        destination_dir = self.source_dir / category
        self._move_file(item, destination_dir, dry_run)

    def _handle_duplicate(self, item: Path, dry_run: bool):
        """Moves a duplicate file to the duplicates directory."""
        self.report_data["summary"]["duplicates_found"] += 1
        if not dry_run:
            self.duplicates_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(self.duplicates_dir / item.name))
        action = {"file": item.name, "action": "moved_to_duplicates", "destination": str(self.duplicates_dir)}
        self.report_data["actions"].append(action)
        logging.info(f"Moved duplicate '{item.name}' to {self.duplicates_dir}")

    def _archive_old_file(self, item: Path, dry_run: bool) -> bool:
        """Archives the file if it's older than the configured threshold."""
        if not self.archive_config.get("enabled"):
            return False

        older_than_days = self.archive_config.get("older_than_days", 90)
        archive_folder = Path(self.archive_config.get("archive_folder", '~/Desktop/Archived')).expanduser()
        
        file_mod_time = datetime.fromtimestamp(item.stat().st_mtime)
        if datetime.now() - file_mod_time > timedelta(days=older_than_days):
            logging.info(f"Archiving old file: {item.name}")
            self.report_data["summary"]["archives_created"] += 1
            if not dry_run:
                archive_folder.mkdir(exist_ok=True)
                shutil.make_archive(str(archive_folder / item.stem), 'zip', item.parent, item.name)
                item.unlink() # Delete original file after archiving
            action = {"file": item.name, "action": "archived", "destination": str(archive_folder)}
            self.report_data["actions"].append(action)
            return True
        return False

    def _move_file(self, source_path: Path, dest_dir: Path, dry_run: bool):
        """Moves a file to a destination, handling name conflicts."""
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)

        destination_path = dest_dir / source_path.name
        if destination_path.exists():
            if self.duplicate_strategy == 'rename':
                destination_path = get_unique_filename(destination_path)
            else: # 'skip'
                logging.info(f"Skipping '{source_path.name}', file already exists in destination.")
                return

        logging.info(f"Moving '{source_path.name}' to '{dest_dir.name}/'")
        if not dry_run:
            shutil.move(str(source_path), str(destination_path))
        
        self.report_data["summary"]["files_moved"] += 1
        action = {"file": source_path.name, "action": "moved", "destination": str(dest_dir)}
        self.report_data["actions"].append(action)

    def clean(self, dry_run: bool = False):
        """Scans the source directory and processes all files in parallel."""
        start_time = time.time()
        logging.info(f"Starting cleanup in '{self.source_dir}'... (Dry run: {dry_run})")

        files_to_process = [item for item in self.source_dir.iterdir() if item.is_file()]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._process_file, item, dry_run) for item in files_to_process]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"An error occurred while processing a file: {e}", exc_info=True)

        logging.info(f"Cleanup finished in {time.time() - start_time:.2f} seconds.")