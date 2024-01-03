from datetime import datetime
from sqlite3 import Connection, Row
import os


class TodoService():
    def __init__(self, connection: Connection) -> None:
        self.dirname = os.path.dirname(__file__)
        self.conn = connection
        self.cur = self.conn.cursor()

    def create_todo(self, title: str, details: str, checked: bool):
        data = {"title": title, "details": details, "checked": checked}
        id = self.conn.execute(self._readsql("create_one.sql"), data).lastrowid
        self.conn.commit()
        return self.find_unique(id)

    def update_todo(self, id: int, title: str, details: str, checked: bool):
        data = {
            "title": title,
            "details": details,
            "checked": checked,
            "updated_at": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "id": id
        }
        self.cur.execute(self._readsql("update_one.sql"), data)
        self.conn.commit()
        return self.find_unique(id)

    def delete_todo(self, id: int):
        item = self.find_unique(id)
        data = {'id': id}
        self.cur.execute(self._readsql("delete_one.sql"), data)
        return item

    def find_all(self):
        item = self.cur.execute(self._readsql("select_all.sql"))
        return self._to_dict(item.fetchall())

    def find_unique(self, id: int):
        data = {'id': id}
        item = self.cur.execute(self._readsql("select_one.sql"), data)
        return self._to_dict(item.fetchone())

    def _readsql(self, path: str):
        fullpath = os.path.join(self.dirname, "sql", path)
        with open(fullpath, "r") as sql:
            return sql.read()

    def _to_dict(self, todo):
        columns = [col[0] for col in self.cur.description]
        if isinstance(todo, tuple):
            return dict(zip(columns, todo))
        else:
            return [dict(zip(columns, row)) for row in todo]
