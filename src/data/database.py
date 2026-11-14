"""Database manager for SQLite storage operations."""

import sqlite3

import pandas as pd


class DatabaseManager:
    """Manages the SQLite connection and CRUD operations for transactions."""

    _TABLE = "transactions"

    def __init__(self, db_path: str = "finanzas.db") -> None:
        """Initializes the database manager with the SQLite file path."""
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Opens and returns a new SQLite connection."""
        return sqlite3.connect(
            self._db_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

    def init_db(self) -> None:
        """Creates the transactions table if it does not already exist."""
        with self._get_connection() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._TABLE} (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    date        TEXT    NOT NULL,
                    amount      REAL    NOT NULL,
                    category    TEXT    NOT NULL,
                    description TEXT
                )
            """)

    def clear_database(self) -> None:
        """Drops and recreates the transactions table."""
        with self._get_connection() as conn:
            conn.execute(f"DROP TABLE IF EXISTS {self._TABLE}")
        self.init_db()

    def insert_transaction(
        self,
        date: str,
        amount: float,
        category: str,
        description: str,
    ) -> None:
        """Inserts a single transaction record into the database."""
        with self._get_connection() as conn:
            conn.execute(
                f"INSERT INTO {self._TABLE} (date, amount, category, description)"
                " VALUES (?, ?, ?, ?)",
                (date, amount, category, description),
            )

    def insert_many(self, records: list) -> None:
        """Bulk-inserts multiple transaction records in a single batch."""
        with self._get_connection() as conn:
            conn.executemany(
                f"INSERT INTO {self._TABLE} (date, amount, category, description)"
                " VALUES (?, ?, ?, ?)",
                records,
            )

    def get_all_transactions(self) -> pd.DataFrame:
        """Retrieves all transactions as a DataFrame ordered by date descending."""
        with self._get_connection() as conn:
            return pd.read_sql_query(
                f"SELECT * FROM {self._TABLE} ORDER BY date DESC",
                conn,
                parse_dates=["date"],
            )

    def count(self) -> int:
        """Returns the total number of rows in the transactions table."""
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {self._TABLE}")
            return cursor.fetchone()[0]
