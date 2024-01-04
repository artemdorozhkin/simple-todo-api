import sqlite3
from pathlib import Path
from os import listdir
from flask import current_app

from api.helpers.utils import readsql


dirname = Path(__file__).parent
DEFAULT_PATH = Path.joinpath(dirname, "default.db")


def create_connection(db_path=DEFAULT_PATH):
    queries_path = Path.joinpath(dirname, "tables")

    connection = sqlite3.connect(db_path, check_same_thread=False)
    for queri in listdir(queries_path):
        connection.execute(readsql(Path.joinpath(queries_path, queri)))
        print(f"table {Path(queri).stem} created")

    return connection
