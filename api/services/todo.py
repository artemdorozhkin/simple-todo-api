from datetime import datetime
from sqlite3 import Connection, Row


class TodoService():
    def __init__(self, connection: Connection) -> None:
        self.conn = connection
        self.cur = self.conn.cursor()

    def create_todo(self, title: str, details: str, checked: bool):
        query = """
            INSERT INTO todos (title, details, checked)
            VALUES (?, ?, ?);
        """
        id = self.conn.execute(query, (title, details, checked)).lastrowid
        self.conn.commit()
        return self.find_unique(id)

    def update_todo(self, id: int, title: str, details: str, checked: bool):
        query = """
            UPDATE todos
            SET title = ?,
                details = ?,
                checked = ?,
                updated_at = ?
            WHERE id = ?;
        """
        self.cur.execute(query, (
            title,
            details,
            checked,
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            id
        ))
        self.conn.commit()
        return self.find_unique(id)

    def delete_todo(self, id: int):
        query = """
            DELETE FROM todos
            WHERE id = ?;
        """
        data = self.find_unique(id)
        self.cur.execute(query, (id,))
        return data

    def find_all(self):
        query = """
            SELECT *
            FROM todos;
        """
        data = self.cur.execute(query)
        return [self._to_dict(item) for item in data]

    def find_unique(self, id: int):
        query = """
            SELECT *
            FROM todos
            WHERE id = ?;
        """
        data = self.cur.execute(query, (id,))
        return self._to_dict(data.fetchone())

    def _to_dict(self, todo: tuple):
        return {
            "id": todo[0],
            "title": todo[1],
            "details": todo[2],
            "checked": todo[3],
            "created_at": todo[4],
            "updated_at": todo[5],
        }
