""" import sqlite3
from typing import Optional, List, Dict, Any
import os

class DatabaseHandler:
    def __init__(self, db_path: str = "instance/app.db"):
        self.db_path = db_path
        self._create_db_directory()

    def _create_db_directory(self):
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute(query, params)
            return cursor.fetchall()

    def create_tables(self, schema_path: str = None):
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()
"""