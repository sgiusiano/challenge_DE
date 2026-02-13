import os
import logging
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from pymongo import MongoClient
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages PostgreSQL and MongoDB connections."""

    def __init__(self) -> None:
        self.mongo_client: MongoClient | None = None

    @contextmanager
    def get_connection(self) -> Generator:
        """Context manager for PostgreSQL connections."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                port=os.environ.get("POSTGRES_PORT"),
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
            )
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def init_database(self) -> None:
        """Initialize the database schema from SQL script."""
        script_file = Path(__file__).parent / "init_db.sql"
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(script_file.read_text())
                conn.commit()

    def init_mongo(self) -> None:
        """Initialize MongoDB connection."""
        try:
            mongo_uri = os.environ.get("MONGO_URI")
            self.mongo_client = MongoClient(mongo_uri)
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise

    def clean_event_collection(self) -> None:
        """Delete all events from the MongoDB collection."""
        collection = self.get_event_collection()
        collection.delete_many({})

    def get_event_collection(self) -> Collection:
        """Get the MongoDB events collection."""
        if not self.mongo_client:
            self.init_mongo()
        db = self.mongo_client["challenge"]
        return db["events"]
