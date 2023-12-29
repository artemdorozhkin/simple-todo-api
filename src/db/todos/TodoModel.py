from datetime import datetime
from pathlib import Path
from string import Template
from ..helpers.helpers import read_sql
from db.DBService import DBService


DIRNAME = Path.joinpath(Path(__file__).parent, 'sql')

def create_path(filename: str) -> Path:
    return Path.joinpath(DIRNAME, filename)

queries = {
    "create_table": read_sql(create_path('create_table.sql')),
    "find_all": read_sql(create_path('find_all.sql')),
    "find_unique": read_sql(create_path('find_unique.sql')),
    "create_todo": read_sql(create_path('create_todo.sql')),
    "update_todo": read_sql(create_path('update_todo.sql')),
    "delete_todo": read_sql(create_path('delete_todo.sql')),
    "drop_table": read_sql(create_path('drop_table.sql')),
}

class TodoModel():
    _db = None

    def __init__(self, db: DBService) -> None:
        self._db = db
        self.create_table()
    
    def create_table(self):
        self._db.cursor.execute(queries['create_table'])

    def drop_table(self):
        self._db.cursor.execute(queries['drop_table'])

    def create_todo(self, title: str, details: str, checked: bool):
        query = Template(queries['create_todo']).substitute(
            title=title,
            details=details,
            checked=checked,
        )
        self._commit(query)
        todos = self.find_all()
        return todos[len(todos) - 1]

    def update_todo(self, id: int, title: str, details: str, checked: bool):
        query = Template(queries['update_todo']).substitute(
            id=id,
            title=title,
            details=details,
            checked=checked,
            updated_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        )
        self._commit(query)
        return self.find_unique(id)

    def delete_todo(self, id: int):
        todo = self.find_unique(id)
        if todo:
            query = Template(queries['delete_todo']).substitute(id=id)
            self._commit(query)
        return todo

    def find_all(self):
        return self._db.cursor.execute(queries['find_all']).fetchall()

    def find_unique(self, id: int):
        return self._db.cursor.execute(Template(queries['find_unique']).substitute(id=id)).fetchall()

    def _commit(self, query: str):
        self._db.cursor.execute(query)
        self._db.connection.commit()
