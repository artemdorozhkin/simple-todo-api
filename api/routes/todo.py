from flask import Blueprint, make_response, request, current_app

from api.db.db_utils import db
from api.helpers.http.json_response import http_response
from api.helpers.http.statuscodes import BAD_REQUEST, CREATED, NO_CONTENT, OK
from api.routes.auth import auth
from api.services.todo import TodoService
from api.services.todo.exceptions import IncorrectData, ItemNotExists


todo = Blueprint('todos', __name__, url_prefix="/todos")
todo_serice = TodoService(db)


@todo.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    current_app.logger.info("getting todos...")
    if request.method == 'GET':
        items = todo_serice.findall()
        if len(items) == 0:
            return make_response(items, NO_CONTENT)
        else:
            return make_response(items, OK)
    else:
        current_app.logger.info("creating todos...")
        try:
            todoitem = todo_serice.create(
                title=request.form['title'],
                details=request.form['details'],
                checked=request.form['checked'],
            )
            return make_response(todoitem, CREATED)
        except IncorrectData as e:
            current_app.logger.error(e.args[0])
            return http_response(BAD_REQUEST, e.args[0])


@todo.route('/<int:id>', methods=['GET'])
@auth.login_required
def get_todo(id: int):
    current_app.logger.info(f"getting todo {id}...")
    try:
        item = todo_serice.findone(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])


@todo.route('/<int:id>', methods=['PUT'])
@auth.login_required
def update_todo(id: int):
    current_app.logger.info(f"updating todo {id}...")
    try:
        item = todo_serice.update(
            id=id,
            title=request.form['title'],
            details=request.form['details'],
            checked=request.form['checked'],
        )
        return make_response(item, OK)
    except IncorrectData as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])


@todo.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_todo(id: int):
    current_app.logger.info(f"deleting todo {id}...")
    try:
        item = todo_serice.delete(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])
