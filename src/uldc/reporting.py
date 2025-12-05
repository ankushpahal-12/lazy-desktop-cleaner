import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def generate_report(report_data: Dict[str, Any], output_dir: Path):
    """Generates a JSON summary report of the cleaning operation."""
    report_data["summary"]["report_generated_at"] = datetime.now().isoformat()
    report_filename = f"cleaning_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path = output_dir / report_filename

    try:
        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2)
        logging.info(f"Successfully generated report: {report_path}")
    except IOError as e:
        logging.error(f"Failed to write report to {report_path}: {e}")