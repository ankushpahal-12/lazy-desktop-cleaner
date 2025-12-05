import argparse
import logging
from pathlib import Path
import yaml
from .categorizer import FileCategorizer
from .organizer import DesktopOrganizer
from .reporting import generate_report


def setup_logging(log_file: str):
    """Configures logging to both console and a file."""
    log_path = Path(log_file).expanduser()
    log_path.parent.mkdir(exist_ok=True, parents=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

def load_config(path: str = 'config.yaml'):
    """Loads the YAML configuration file."""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at '{path}'. Please create it.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise

def main():
    """Main function to configure and run the desktop cleaner."""
    parser = argparse.ArgumentParser(description="Automatically organize files in a directory.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the cleaning process without moving files.")
    parser.add_argument("--config", default="config.yaml", help="Path to the configuration file.")
    args = parser.parse_args()

    try:
        # setup_logging is called first to ensure any subsequent errors are logged.
        # A default path is used if the config can't be read.
        # This is a bit of a chicken-and-egg problem, but this way we always have logs.
        try:
            app_config = load_config(args.config)
            setup_logging(app_config.get('log_file', 'organizer.log'))
        except (FileNotFoundError, yaml.YAMLError):
            setup_logging('organizer.log') # Fallback log file
            # Re-raise the exception to be caught by the outer block
            raise

        app_config = load_config(args.config)
        source_directory = Path(app_config['source_directory']).expanduser()
        
        categorizer = FileCategorizer(app_config['categories'])
        organizer = DesktopOrganizer(source_directory, categorizer, app_config)

        organizer.clean(dry_run=args.dry_run)
        generate_report(organizer.report_data, source_directory)

    except (FileNotFoundError, yaml.YAMLError):
        # Errors from load_config are already logged, so we can just exit gracefully.
        logging.critical("Halting execution due to configuration error.")
    except KeyError as e:
        logging.critical(f"Configuration error: Missing required key {e}. Please check your config.yaml.")
    except Exception as e:
        logging.critical(f"An unexpected and fatal error occurred: {e}", exc_info=True)

if __name__ == '__main__':
    main()