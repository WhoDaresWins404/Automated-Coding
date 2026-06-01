import polars as pl
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

# Import our storage layer
from core.storage import DataStorage
from config.settings import settings

class DataCollector:
    """
    Semi-automatic data collector.
    - Ingests raw data (CSV/JSON/Parquet).
    - Validates schema.
    - Saves to Parquet with 'pending' status.
    - Requires human approval before training.
    """

    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, file_path: str, file_format: str = "auto") -> pl.DataFrame:
        """
        Loads raw data from a file.
        Supports: CSV, JSON, Parquet.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_format == "auto":
            suffix = file_path.suffix.lower()
            if suffix == ".csv":
                file_format = "csv"
            elif suffix == ".json":
                file_format = "json"
            elif suffix == ".parquet":
                file_format = "parquet"
            else:
                raise ValueError(f"Unsupported file format: {suffix}")

        try:
            if file_format == "csv":
                df = pl.read_csv(file_path)
            elif file_format == "json":
                df = pl.read_json(file_path)
            elif file_format == "parquet":
                df = pl.read_parquet(file_path)
            else:
                raise ValueError(f"Unknown format: {file_format}")
            
            return df
        except Exception as e:
            raise ValueError(f"Failed to load data from {file_path}: {e}")

    def validate_schema(self, df: pl.DataFrame, expected_columns: Optional[List[str]] = None) -> bool:
        """
        Basic schema validation.
        - Checks if expected columns exist.
        - Checks for nulls in critical columns (if defined).
        """
        if expected_columns:
            missing = [col for col in expected_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Missing expected columns: {missing}")
        
        # Example: Check for nulls in first column (could be made configurable)
        if df.shape > 0:
            null_counts = df.null_count()
            if null_counts > 0:
                print(f"⚠️  Warning: {null_counts} nulls found in first column.")
        
        return True

    def collect_and_store(
        self, 
        file_path: str, 
        name: str, 
        expected_columns: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Main workflow: Load -> Validate -> Save (Pending) -> Log.
        Returns the dataset ID or name.
        """
        # 1. Load
        df = self.load_data(file_path)
        print(f"✅ Loaded {len(df)} rows from {file_path}")

        # 2. Validate
        self.validate_schema(df, expected_columns)
        print("✅ Schema validation passed")

        # 3. Save to Parquet (Pending Status)
        dataset_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        parquet_path = self.storage.save_dataset_to_parquet(df, dataset_name)
        
        # Note: save_dataset_to_parquet currently sets status='approved' in memory.
        # We will override this to 'pending' for the semi-automatic workflow.
        self._mark_as_pending(dataset_name)

        # 4. Log Metadata
        if metadata:
            self._log_metadata(dataset_name, metadata)

        print(f"📦 Dataset '{dataset_name}' saved to {parquet_path} (Status: Pending)")
        return dataset_name

    def _mark_as_pending(self, name: str):
        """
        Updates the database to mark a dataset as 'pending' approval.
        """
        conn = self.storage.db_path.__class__.connect(self.storage.db_path) # Quick hack for demo
        # In real code, use the storage class's DB connection method
        cursor = conn.cursor()
        cursor.execute("UPDATE datasets SET status = 'pending' WHERE name = ?", (name,))
        conn.commit()
        conn.close()

    def _log_metadata(self, name: str, metadata: Dict[str, Any]):
        """
        Logs additional metadata to the database.
        """
        # Placeholder for extending the DB schema later
        pass

    def list_pending_datasets(self) -> List[Dict[str, Any]]:
        """
        Returns a list of datasets waiting for approval.
        """
        conn = self.storage.db_path.__class__.connect(self.storage.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, created_at, row_count FROM datasets WHERE status = 'pending'")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row,
                "name": row,
                "created_at": row,
                "row_count": row
            }
            for row in rows
        ]

    def approve_dataset(self, dataset_id: int):
        """
        Human approval step: Marks dataset as 'approved' for training.
        """
        conn = self.storage.db_path.__class__.connect(self.storage.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE datasets SET status = 'approved' WHERE id = ?", (dataset_id,))
        conn.commit()
        conn.close()
        print(f"✅ Dataset ID {dataset_id} approved for training.")

    def reject_dataset(self, dataset_id: int, reason: str):
        """
        Human rejection step: Marks dataset as 'rejected' and logs reason.
        """
        conn = self.storage.db_path.__class__.connect(self.storage.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE datasets SET status = 'rejected', rejection_reason = ? WHERE id = ?", (reason, dataset_id))
        conn.commit()
        conn.close()
        print(f"❌ Dataset ID {dataset_id} rejected: {reason}")

# Example Usage (for testing)
if __name__ == "__main__":
    storage = DataStorage()
    collector = DataCollector(storage)
    
    # Example: Collect a CSV file
    # collector.collect_and_store("data/sample.csv", "sample_run", expected_columns=["id", "value"])
    
    # List pending datasets
    pending = collector.list_pending_datasets()
    print(f"Pending datasets: {pending}")