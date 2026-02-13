import json
import logging
from pathlib import Path

from src.storage.database import DatabaseManager

logger = logging.getLogger(__name__)


class LogReader:
    """Reads and validates JSON log files from the events directory."""

    def __init__(self, events_dir: str, db_manager: DatabaseManager) -> None:
        self.events_dir = Path(events_dir)
        self.db_manager = db_manager

    def read_logs(self) -> None:
        """Read all JSON log files from the events directory."""
        for file_path in self.events_dir.glob("*.json"):
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    for event in data:
                        if isinstance(event, dict):
                            event["_source_file"] = str(file_path)
                            self.db_manager.get_event_collection().insert_one(event)
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
