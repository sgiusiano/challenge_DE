import logging
import os
import sys

from src.ingestion.log_reader import LogReader
from src.storage.database import DatabaseManager
from src.transformation.ingestion import EventIngestion
from src.transformation.transformation import ETLTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def run_ingestion(self) -> None:
        """Run the ingestion process."""
        logger.info("Reading raw log files and ingesting into MongoDB...")
        log_reader = LogReader(os.environ.get("RAW_FILE_PATH", "data/events/"), self.db_manager)
        log_reader.read_logs()
        logger.info("Ingestion into MongoDB complete.")

    def run_transformation(self) -> None:
        """Run the transformation process."""
        logger.info("Starting data transformation process...")

        logger.info("Step 1: Ingesting events from MongoDB for transformation.")
        ingestion = EventIngestion(self.db_manager)
        ingestion.ingest_events()

        logger.info("Step 2: Running main ETL transformations to build trusted layer.")
        etl_process = ETLTransformer(self.db_manager)
        etl_process.run_etl()

        logger.info("Step 3: Building data marts.")
        etl_process.run_marts()

        logger.info("Data transformation process completed.")

    def run(self) -> None:
        """Run the entire pipeline."""
        logger.info("Initializing database schema...")
        self.db_manager.init_database()
        logger.info("Starting ingestion from files to raw layer...")
        self.run_ingestion()
        logger.info("Starting transformation from raw to trusted and mart layers...")
        self.run_transformation()


if __name__ == "__main__":
    logger.info("ETL Pipeline Started.")
    db_manager = DatabaseManager()
    pipeline = Pipeline(db_manager)
    pipeline.run()
    logger.info("ETL Pipeline Finished Successfully.")
