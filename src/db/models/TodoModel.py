from datetime import datetime
from pathlib import Path
from string import Template
from ..helpers.helpers import read_sql
from db.DBService import DBService


class TodoModel():
    _db = None

    def __init__(self, db: DBService) -> None:
        self._db = db

    def create_todo(self, title: str, details: str, checked: bool):
        query = """
            INSERT INTO todos (title, details, checked)
            VALUES (?, ?, ?);
        """
        data = self._db.cursor.execute(query, (title, details, checked))
        self._db.connection.commit()
        return data.fetchone()

    def update_todo(self, id: int, title: str, details: str, checked: bool):
        query = """
            UPDATE todos
            SET title = ?,
                details = ?,
                checked = ?,
                updated_at = ?
            WHERE id = ?;
        """
        data = self._db.cursor.execute(query, (
            title,
            details,
            checked,
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            id
        ))
        self._db.connection.commit()
        return data.fetchone()

    def delete_todo(self, id: int):
        query = """
            DELETE FROM todos
            WHERE id = ?;
        """
        data = self._db.cursor.execute(query, (id))
        return data.fetchone()

    def find_all(self):
        query = """
            SELECT *
            FROM todos;
        """
        data = self._db.cursor.execute(query)
        return data.fetchall()

    def find_unique(self, id: int):
        query = """
            SELECT *
            FROM todos
            WHERE id = ?;
        """
        data = self._db.cursor.execute(query, (id))
        return data.fetchone()

