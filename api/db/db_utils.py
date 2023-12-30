import sqlite3
from pathlib import Path


DEFAULT_PATH = Path.joinpath(Path(__file__).parent, "default.db")
def create_connection(db_path = DEFAULT_PATH):
    create_table = """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            details TEXT,
            checked BOOLEAN,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    connection = sqlite3.connect(db_path, check_same_thread=False)
    connection.execute(create_table)
    return connection
