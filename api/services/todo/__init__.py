from datetime import datetime
from sqlite3 import Connection
from os.path import dirname, join
from api.helpers.utils import readsql, to_dict

from api.services.todo.exceptions import IncorrectData, ItemNotExists


class TodoService():
    def __init__(self, connection: Connection) -> None:
        self.dirname = dirname(__file__)
        self.queries_path = join(self.dirname, "sql")
        self.conn = connection
        self.cur = self.conn.cursor()

    def create_todo(self, title: str, details: str, checked: str):
        if not self._valide_title(title):
            raise IncorrectData("title can't be null and must be a string")

        if not checked.lower() in ('true', 'false'):
            raise IncorrectData("checked must be bool")

        data = {"title": title, "details": details, "checked": bool(checked)}
        id = self.conn.execute(
            readsql(join(self.queries_path, "create_one.sql")), data
        ).lastrowid
        self.conn.commit()
        return self.find_unique(id)

    def update_todo(self, id: int, title: str, details: str, checked: str):
        if not self._valide_title(title):
            raise IncorrectData("title can't be null and must be a string")

        if not checked.lower() in ('true', 'false'):
            raise IncorrectData("checked must be bool")

        data = {
            "title": title,
            "details": details,
            "checked": bool(checked),
            "updated_at": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "id": id
        }
        self.cur.execute(
            readsql(join(self.queries_path, "update_one.sql")), data)
        self.conn.commit()
        return self.find_unique(id)

    def delete_todo(self, id: int):
        item = self.find_unique(id)

        data = {'id': id}
        self.cur.execute(
            readsql(join(self.queries_path, "delete_one.sql")), data)

        return item

    def find_all(self):
        item = self.cur.execute(
            readsql(join(self.queries_path, "select_all.sql"))
        )
        return to_dict(item.fetchall())

    def find_unique(self, id: int):
        data = {'id': id}
        item = self.cur.execute(
            readsql(join(self.queries_path, "select_one.sql")), data
        ).fetchone()

        if not item:
            raise ItemNotExists(f"todo with id {id} not found")

        return to_dict(item)

    def _valide_title(self, title: str) -> bool:
        return isinstance(title, str) and len(title) > 0
