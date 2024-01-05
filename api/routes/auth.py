from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

from api.helpers.http.statuscodes import BAD_REQUEST, CONFLICT, CREATED
from api.services.user import UserService
from api.db.db_utils import db
from api.helpers.http.json_response import http_response


auth = Blueprint('auth', __name__)
userService: UserService = UserService(db)


@auth.route("/login")
def login():
    pass


@auth.route("/signup", methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    hash = generate_password_hash(password)

    try:
        user = userService.create(email, hash)
        if not user:
            raise Exception("Unexpected error. User not created.")

        return http_response(
            CREATED,
            "User successfully created",
        )
    except Exception as e:
        return http_response(
            BAD_REQUEST,
            f"An error occurred during user creation: {e.args[0]}",
        )


@auth.route("/logout")
def logout():
    pass
