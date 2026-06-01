import polars as pl
import sqlite3
from pathlib import Path
from datetime import datetime

class DataStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "metadata.db"
        self.init_db()

    def init_db(self):
        """Initialize SQLite database for metadata."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                row_count INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER,
                model_architecture TEXT,
                hyperparameters TEXT,
                metrics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
            )
        """)
        conn.commit()
        conn.close()

    def save_dataset_to_parquet(self, df: pl.DataFrame, name: str) -> str:
        """Save a Polars DataFrame to a Parquet file."""
        file_path = self.data_dir / f"{name}.parquet"
        df.write_parquet(file_path)
        
        # Log to SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO datasets (name, row_count, status) VALUES (?, ?, ?)",
            (name, len(df), "approved")
        )
        conn.commit()
        conn.close()
        return str(file_path)

    def load_dataset_from_parquet(self, name: str) -> pl.DataFrame:
        """Load a Parquet file into a Polars DataFrame."""
        file_path = self.data_dir / f"{name}.parquet"
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset {name} not found.")
        return pl.read_parquet(file_path)