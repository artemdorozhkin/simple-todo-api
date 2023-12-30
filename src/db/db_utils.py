import sqlite3
from pathlib import Path


DEFAULT_PATH = Path.joinpath(Path(__file__).parent, "default.db")
def create_connection(db_path = DEFAULT_PATH):
    return sqlite3.connect(db_path, check_same_thread=False)
