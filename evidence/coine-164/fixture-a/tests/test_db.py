import tempfile
import unittest
from pathlib import Path

from app.db import Database


class DatabaseTest(unittest.TestCase):
    def test_list_rates_returns_empty_list_for_unknown_base(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "test.db")
            database.init_schema()
            self.assertEqual(database.list_rates("EUR"), [])


if __name__ == "__main__":
    unittest.main()
