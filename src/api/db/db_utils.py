import sqlite3
from pathlib import Path
from os import listdir

from api.helpers.utils import readsql


dirname = Path(__file__).parent
DEFAULT_PATH = Path.joinpath(dirname, "default.db")


def create_connection(db_path=DEFAULT_PATH):
    queries_path = Path.joinpath(dirname, "tables")
    migrations_path = Path.joinpath(dirname, "migrations")

    connection = sqlite3.connect(db_path, check_same_thread=False)
    for queri in listdir(queries_path):
        connection.execute(readsql(Path.joinpath(queries_path, queri)))

    for migration in listdir(migrations_path):
        try:
            connection.execute(
                readsql(Path.joinpath(migrations_path, migration))
            )
        except Exception as e:
            pass

    return connection


db_path = Path.joinpath(Path.cwd(), "db", "todos.db")
db_path.parent.mkdir(parents=True, exist_ok=True)
db = create_connection(db_path=db_path)
