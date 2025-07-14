
import os
from src.storage.database import DatabaseManager

class etl:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def run_etl(self):
        """Run the ETL process."""
        queries_dir = os.path.join(os.path.dirname(__file__), 'queries')
        users_query = os.path.join(queries_dir, 'load_trusted_users.sql')
        documents_query = os.path.join(queries_dir, 'load_trusted_documents.sql')
        event_query = os.path.join(queries_dir, 'load_trusted_events.sql')
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                with open(users_query, 'r') as f:
                    cur.execute(f.read())
                    conn.commit()
                with open(documents_query, 'r') as f:
                    cur.execute(f.read())
                    conn.commit()
                with open(event_query, 'r') as f:
                    cur.execute(f.read())
                    conn.commit()

    def run_marts(self):
        """Run the marts loading"""
        queries_dir = os.path.join(os.path.dirname(__file__), 'queries')
        load_sessions_query = os.path.join(queries_dir, 'load_sessions.sql')
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                with open(load_sessions_query, 'r') as f:
                    cur.execute(f.read())
                    conn.commit()
