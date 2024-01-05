from datetime import datetime
from sqlite3 import Connection
from os.path import dirname, join
from api.helpers.utils import readsql
from api.services.user.exceptions import UserNotFound


class User:
    def __init__(self, email: str, hash: str, token: str = "") -> None:
        self.email = email
        self.hash = hash
        self.token = token


def to_user(result):
    if isinstance(result, tuple):
        return User(result[1], result[2], result[3])
    else:
        return [User(row[1], row[2], result[3]) for row in result]


class UserService():
    def __init__(self, connection: Connection) -> None:
        self.dirname = dirname(__file__)
        self.queries_path = join(self.dirname, "sql")
        self.conn = connection
        self.cur = self.conn.cursor()

    def create(self, email: str, hash: str):
        data = {"email": email, "hash": hash, "token": None}
        id = self.conn.execute(
            readsql(join(self.queries_path, "create_one.sql")), data
        ).lastrowid
        self.conn.commit()
        return self.findone(email)

    def updatetoken(self, email: str, token: str):
        data = {
            "token": token,
            "updated_at": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "email": email
        }

        self.cur.execute(
            readsql(join(self.queries_path, "update_token.sql")), data)
        self.conn.commit()

        return self.findone(email)

    def delete(self, email: str):
        user = self.findone(email)

        data = {'email': email}
        self.cur.execute(
            readsql(join(self.queries_path, "delete_one.sql")), data
        )

        return user

    def findall(self):
        user = self.cur.execute(
            readsql(join(self.queries_path, "select_all.sql"))
        )
        return to_user(user.fetchall())

    def findone(self, email: str) -> User:
        data = {'email': email}
        user = self.cur.execute(
            readsql(join(self.queries_path, "select_one.sql")), data
        ).fetchone()

        if not user:
            return None

        return to_user(user)
