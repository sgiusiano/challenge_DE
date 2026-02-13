from pathlib import Path

from src.storage.database import DatabaseManager

QUERIES_DIR = Path(__file__).parent / "queries"


class ETLTransformer:
    """Orchestrates SQL-based transformations from raw to trusted and mart layers."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def _execute_sql_file(self, file_path: Path) -> None:
        """Execute a SQL file within a transaction."""
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(file_path.read_text())
                conn.commit()

    def run_etl(self) -> None:
        """Run ETL transformations to build the trusted layer."""
        self._execute_sql_file(QUERIES_DIR / "load_trusted_users.sql")
        self._execute_sql_file(QUERIES_DIR / "load_trusted_documents.sql")
        self._execute_sql_file(QUERIES_DIR / "load_trusted_events.sql")

    def run_marts(self) -> None:
        """Build data marts from trusted layer."""
        self._execute_sql_file(QUERIES_DIR / "load_sessions.sql")
