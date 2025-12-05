import logging
from pathlib import Path
from typing import Dict, List

try:
    import magic
except ImportError:
    # Provide a fallback for systems where python-magic might be tricky to install
    logging.warning("python-magic not found. Falling back to extension-based categorization.")
    magic = None


class FileCategorizer:
    """Categorizes files based on MIME types or extensions."""

    def __init__(self, extension_mappings: Dict[str, List[str]]):
        self.extension_mappings = extension_mappings

    def categorize(self, file_path: Path) -> str:
        """
        Determines the category of a file.
        Uses MIME type if available, otherwise falls back to file extension.
        """
        if magic:
            mime_type = magic.from_file(str(file_path), mime=True)
            for category, mimes in self.extension_mappings.items():
                if any(m in mime_type for m in mimes):
                    return category
        return "Other"