# src/uldc/config.py
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: Path = Path('config.yaml')) -> Dict[str, Any]:
    """
    Loads and validates the YAML configuration file.

    Args:
        config_path: The path to the configuration file.

    Returns:
        A dictionary containing the configuration settings.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If essential keys are missing from the config.
    """
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Validate essential keys
    if 'source_directory' not in config or 'categories' not in config:
        raise ValueError("Config must contain 'source_directory' and 'categories' keys.")

    # Expand the '~' user home directory symbol and ensure it's a Path object
    config['source_directory'] = Path(config['source_directory']).expanduser()

    return config

def get_category_mappings(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Creates a reverse map from file extension to category folder for quick lookups.
    Example: {'.jpg': 'Images', '.pdf': 'Documents'}

    Args:
        config: The application configuration dictionary.

    Returns:
        A dictionary mapping file extensions to category names.
    """
    extension_to_category = {}
    for category, extensions in config.get('categories', {}).items():
        for ext in extensions:
            # Ensure extensions are lowercase for case-insensitive matching
            extension_to_category[ext.lower()] = category
    return extension_to_category

