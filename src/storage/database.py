import psycopg2
import logging
from contextlib import contextmanager
from pymongo import MongoClient
import pandas as pd
import os

logger = logging.getLogger(__name__)

class DatabaseManager:

    def __init__(self):
        self.connection = None
        self.mongo_client = None

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT'),
                dbname=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize the database."""
        script_file = os.path.join(os.path.dirname(__file__), 'init_db.sql')
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                with open(script_file, 'r') as f:
                    cur.execute(f.read())
                    conn.commit()
    
    def init_mongo(self):
        """Initialize MongoDB connection."""
        try:
            mongo_uri = os.environ.get('MONGO_URI')
            self.mongo_client = MongoClient(mongo_uri)
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise
    
    def clean_event_collection(self):
        """Clean a MongoDB collection."""
        if not self.mongo_client:
            self.init_mongo()
        db = self.mongo_client["challenge"]
        collection = db["events"]
        collection.delete_many({})
    
    def get_event_collection(self):
        """Get a MongoDB client."""
        if not self.mongo_client:
            self.init_mongo()
        db = self.mongo_client["challenge"]
        return db["events"]
