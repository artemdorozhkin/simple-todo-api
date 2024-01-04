from flask import make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from api.db.db_utils import db
from api.services.user import UserService, User

auth = HTTPBasicAuth()

userService: UserService = UserService(db)


@auth.verify_password
def verify_password(email: str, password: str):
    print(email)
    if not email:
        return

    user: User = userService.findone(email=email)
    if not user:
        return

    if user and check_password_hash(user.hash, password):
        return email
