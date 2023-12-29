from flask import Flask, request, jsonify

from db.DBService import DBService
from db.todos.TodoModel import TodoModel


app = Flask(__name__)

todo = TodoModel(DBService())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todos = todo.find_all()
        return jsonify(todos)
    else: 
        return jsonify(
            todo.create_todo(
                title=request.form['title'],
                details=request.form['details'],
                checked=request.form['checked'],
            )
        )

@app.route('/todo/<int:id>', methods=['GET'])
def get_todo(id: int):
    return jsonify(todo.find_unique(id))

@app.route('/todo/<int:id>', methods=['PATCH'])
def update_todo(id: int):
    return jsonify(
            todo.update_todo(
                id=id,
                title=request.form['title'],
                details=request.form['details'],
                checked=request.form['checked'],
            )
        )

@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id: int):
    return jsonify(
            todo.delete_todo(id=id)
        )
