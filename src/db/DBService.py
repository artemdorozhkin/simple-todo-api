import sqlite3
from pathlib import Path


class DBService():
    _connection = None
    _cursor = None
    _db_path = ""

    def __init__(self) -> None:
        self._db_path = Path.joinpath(Path.cwd(), "db", "todos.db")
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
        self._cursor = self._connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor
