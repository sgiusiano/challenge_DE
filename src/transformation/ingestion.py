from src.transformation.validators import EventValidator
from src.storage.database import DatabaseManager
from psycopg2.extras import execute_values

class EventIngestion:
     
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def ingest_events(self):
        """Ingest events from MongoDB, validate, and write to PostgreSQL."""
        valid_events = list()
        
        for event in self.db_manager.get_event_collection().find():
            cleaned_event = EventValidator.validate_event(event)
            if cleaned_event:
                valid_events.append(cleaned_event)
        
        # Deduplicate events
        unique_events = EventValidator.deduplicate_events(valid_events)
        
        columns = list(unique_events[0].keys())
        query="INSERT INTO challenge.raw.events ({}) VALUES %s".format(','.join(columns))
        values = [tuple(event[col] for col in columns) for event in unique_events]

        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                execute_values(cur, query, values)
                conn.commit()
        
        self.db_manager.clean_event_collection() #Ya procesamos los documentos y los ingestamos a la BD
