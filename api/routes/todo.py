from pathlib import Path
from flask import Blueprint, request, current_app

from api.db.db_utils import create_connection
from api.services.todo import TodoService


todo = Blueprint('todos', __name__, url_prefix="/todos")

db_path = Path.joinpath(Path.cwd(), "db", "todos.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

todo_serice = TodoService(create_connection(db_path=db_path))


@todo.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return todo_serice.find_all()
    else:
        return todo_serice.create_todo(
            title=request.form['title'],
            details=request.form['details'],
            checked=request.form['checked'],
        )


@todo.route('/<int:id>', methods=['GET'])
def get_todo(id: int):
    return todo_serice.find_unique(id)


@todo.route('/<int:id>', methods=['PUT'])
def update_todo(id: int):
    return todo_serice.update_todo(
        id=id,
        title=request.form['title'],
        details=request.form['details'],
        checked=request.form['checked'],
    )


@todo.route('/<int:id>', methods=['DELETE'])
def delete_todo(id: int):
    return todo_serice.delete_todo(id=id)
