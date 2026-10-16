import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("rates.db")


class Database:
    """Thin wrapper around the SQLite file that stores exchange rates."""

    def __init__(self, path: Path = DEFAULT_DB_PATH) -> None:
        self._path = path

    def connect(self) -> sqlite3.Connection:
        """Open a connection with rows accessible by column name."""
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        return connection

    def init_schema(self) -> None:
        """Create the rates table if it does not exist."""
        with self.connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS rates ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "base TEXT NOT NULL, "
                "quote TEXT NOT NULL, "
                "rate REAL NOT NULL, "
                "fetched_at TEXT NOT NULL)"
            )

    def list_rates(self, base: str) -> list:
        """Return every stored rate for a base currency, newest first."""
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT base, quote, rate, fetched_at FROM rates WHERE base = ? ORDER BY fetched_at DESC",
                (base,),
            ).fetchall()
        return [dict(row) for row in rows]
