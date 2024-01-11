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

    def create(self, title: str, details: str, checked: str, file_path: str):
        if not self._valide_title(title):
            raise IncorrectData("title can't be null and must be a string")

        if not checked.lower() in ('true', 'false'):
            raise IncorrectData("checked must be bool")

        data = {
            "title": title,
            "details": details,
            "checked": checked.lower() == 'true',
            'file_path': file_path
        }
        id = self.conn.execute(
            readsql(join(self.queries_path, "create_one.sql")), data
        ).lastrowid
        self.conn.commit()
        return self.findone(id)

    def update(self, id: int, title: str, details: str, checked: str, file_path: str):
        if not self._valide_title(title):
            raise IncorrectData("title can't be null and must be a string")

        if not checked.lower() in ('true', 'false'):
            raise IncorrectData("checked must be bool")

        data = {
            "title": title,
            "details": details,
            "checked": checked.lower() == 'true',
            "file_path": file_path,
            "updated_at": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "id": id
        }
        self.cur.execute(
            readsql(join(self.queries_path, "update_one.sql")), data)
        self.conn.commit()
        return self.findone(id)

    def delete(self, id: int):
        item = self.findone(id)

        data = {'id': id}
        self.cur.execute(
            readsql(join(self.queries_path, "delete_one.sql")), data)

        return item

    def findall(self, order_by: str, order_direct: str):
        if not order_direct.lower() in ['', 'asc', 'desc']:
            order_direct = 'asc'
        args = ' '.join([order_by, order_direct]).strip()
        query = readsql(join(self.queries_path, "select_all.sql"))
        query = f'{query.replace(";", "")} ORDER BY {args};' if args else query

        item = self.cur.execute(query)
        return to_dict(self.cur.description, item.fetchall())

    def findone(self, id: int):
        data = {'id': id}
        item = self.cur.execute(
            readsql(join(self.queries_path, "select_one.sql")), data
        ).fetchone()

        if not item:
            raise ItemNotExists(f"todo with id {id} not found")

        return to_dict(self.cur.description, item)

    def _valide_title(self, title: str) -> bool:
        return isinstance(title, str) and len(title) > 0
