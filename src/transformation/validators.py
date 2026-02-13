from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EventValidator:
    """Validates and cleans event data."""

    EVENT_REQUIRED_FIELDS = [
        "event_id",
        "timestamp",
        "event_type",
        "user_id",
        "document_id",
    ]

    EVENT_EXPECTED_TYPES = [
        "user_login",
        "document_edit",
        "comment_added",
        "document_shared",
    ]

    EVENT_TYPE_REQUIRED_FIELDS: dict[str, list[str]] = {
        "user_login": ["user_id", "document_id"],
        "document_edit": ["edit_length"],
        "comment_added": ["comment_text"],
        "document_shared": ["shared_with"],
    }

    @staticmethod
    def validate_event(event: dict) -> dict | None:
        """
        Validate event structure and required fields.
        Returns cleaned event or None if invalid.
        """
        event_type = event.get("event_type")
        if str(event_type) not in EventValidator.EVENT_EXPECTED_TYPES:
            logger.error(f"Invalid event type: {event_type}")
            return None

        basic_required = EventValidator.EVENT_REQUIRED_FIELDS
        missing = [field for field in basic_required if field not in event]
        if missing:
            logger.error(f"Missing basic required fields: {missing}")
            return None

        required = EventValidator.EVENT_TYPE_REQUIRED_FIELDS[event_type]
        missing = [field for field in required if field not in event]
        if missing:
            logger.error(f"Missing specific required fields for {event_type}: {missing}")
            return None

        try:
            cleaned_event = {
                "event_id": str(event.get("event_id")),
                "timestamp": event.get("timestamp"),
                "event_type": str(event.get("event_type")),
                "user_id": str(event.get("user_id")),
                "document_id": str(event.get("document_id")),
                "comment_text": str(event.get("comment_text") or ""),
                "edit_length": str(event.get("edit_length") or ""),
                "shared_with": str(event.get("shared_with") or ""),
                "_source_file": str(event.get("_source_file")),
                "_ingested_at": datetime.now().isoformat(),
            }
            return cleaned_event
        except Exception as e:
            logger.error(f"Error creating cleaned event: {e}")
            return None

    @staticmethod
    def deduplicate_events(events: list[dict]) -> list[dict]:
        """Remove duplicate events based on event_id."""
        seen: set[str] = set()
        unique_events: list[dict] = []

        for event in events:
            key = event.get("event_id")

            if key not in seen:
                seen.add(key)
                unique_events.append(event)
            else:
                logger.warning(f"Duplicate event found: {key}")
        return unique_events
