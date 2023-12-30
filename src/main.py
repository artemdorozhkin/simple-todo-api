from pathlib import Path
from flask import Flask, request

from db.db_utils import create_connection
from db.models.TodoModel import TodoService


app = Flask(__name__)
db_path = Path.joinpath(Path.cwd(), "db", "todos.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

todo = TodoService(create_connection(db_path=db_path))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return todo.find_all()
    else: 
        return todo.create_todo(
            title=request.form['title'],
            details=request.form['details'],
            checked=request.form['checked'],
        )


@app.route('/todo/<int:id>', methods=['GET'])
def get_todo(id: int):
    return todo.find_unique(id)


@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id: int):
    return todo.update_todo(
        id=id,
        title=request.form['title'],
        details=request.form['details'],
        checked=request.form['checked'],
    )


@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id: int):
    return todo.delete_todo(id=id)
