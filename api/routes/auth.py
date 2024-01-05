from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from api.helpers.http.statuscodes import BAD_REQUEST, CREATED, OK, UNAUTHORIZED
from api.services.user import UserService
from api.db.db_utils import db
from api.helpers.http.json_response import http_response


auth = Blueprint('auth', __name__)
userService: UserService = UserService(db)


@auth.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = userService.findone(email)
    if not user or not check_password_hash(user.hash, password):
        return http_response(
            UNAUTHORIZED,
            {"msg": "Invalid email or password."}
        )

    token = create_access_token(identity=user.id)
    return http_response(
        OK,
        {"access_token": token}
    )


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
            {"msg": "User successfully created"},
        )
    except Exception as e:
        return http_response(
            BAD_REQUEST,
            {"msg": f"An error occurred during user creation: {e.args[0]}"},
        )


@auth.route("/logout")
def logout():
    pass
