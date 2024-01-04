from pathlib import Path
from flask import Blueprint, make_response, request, current_app

from api.db.db_utils import create_connection
from api.helpers.http.json_response import http_response
from api.helpers.http.statuscodes import BAD_REQUEST, CREATED, NO_CONTENT, OK
from api.services.todo.todo import TodoService
from api.services.todo.exceptions import IncorrectData, ItemNotExists


todo = Blueprint('todos', __name__, url_prefix="/todos")

db_path = Path.joinpath(Path.cwd(), "db", "todos.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

todo_serice = TodoService(create_connection(db_path=db_path))


@todo.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.info("getting todos...")
    if request.method == 'GET':
        items = todo_serice.find_all()
        if len(items) == 0:
            return make_response(items, NO_CONTENT)
        else:
            return make_response(items, OK)
    else:
        current_app.logger.info("creating todos...")
        try:
            todoitem = todo_serice.create_todo(
                title=request.form['title'],
                details=request.form['details'],
                checked=request.form['checked'],
            )
            return make_response(todoitem, CREATED)
        except IncorrectData as e:
            current_app.logger.error(e.args[0])
            return http_response(BAD_REQUEST, e.args[0])


@todo.route('/<int:id>', methods=['GET'])
def get_todo(id: int):
    current_app.logger.info(f"getting todo {id}...")
    try:
        item = todo_serice.find_unique(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])


@todo.route('/<int:id>', methods=['PUT'])
def update_todo(id: int):
    current_app.logger.info(f"updating todo {id}...")
    try:
        item = todo_serice.update_todo(
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
def delete_todo(id: int):
    current_app.logger.info(f"deleting todo {id}...")
    try:
        item = todo_serice.delete_todo(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, e.args[0])
