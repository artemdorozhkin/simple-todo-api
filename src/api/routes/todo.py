from flask import Blueprint, send_from_directory, url_for
from flask import make_response
from flask import request
from flask import current_app

from flask_jwt_extended import jwt_required

from api.db.db_utils import db
from api.helpers.http.json_response import http_response
from api.helpers.http.statuscodes import BAD_REQUEST, CREATED, NO_CONTENT, OK
from api.helpers.utils import save_file
from api.services.todo import TodoService
from api.services.todo.exceptions import IncorrectData, ItemNotExists


todo = Blueprint('todos', __name__, url_prefix="/todos")
todo_serice = TodoService(db)


@todo.route('/', methods=['GET'])
@jwt_required()
def index_get():
    query = request.args
    order_by = query.get('order_by') or ''
    order_direct = query.get('order_direct') or ''

    current_app.logger.info("getting todos...")
    items = todo_serice.findall(order_by, order_direct)
    if len(items) == 0:
        return make_response(items, NO_CONTENT)
    else:
        return make_response(items, OK)


@todo.route('/', methods=['POST'])
@jwt_required()
def index_post():
    current_app.logger.info("creating todos...")
    try:
        json = request.form

        filename = save_file(
            request.files, current_app.config['UPLOAD_FOLDER'])

        url = url_for('todos.uploaded_file',
                      filename=filename
                      ) if filename else ''

        item = todo_serice.create(
            title=json['title'],
            details=json['details'] if 'details' in json else "",
            checked=json['checked'] if 'checked' in json else False,
            file_path=url
        )
        return make_response(item, CREATED)
    except IncorrectData as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, {"msg": e.args[0]})


@todo.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id: int):
    current_app.logger.info(f"getting todo {id}...")
    try:
        item = todo_serice.findone(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, {"msg": e.args[0]})


@todo.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id: int):
    current_app.logger.info(f"updating todo {id}...")
    try:
        json = request.form

        filename = save_file(
            request.files, current_app.config['UPLOAD_FOLDER'])

        url = url_for('todos.uploaded_file',
                      filename=filename
                      ) if filename else ''

        item = todo_serice.update(
            id=id,
            title=json['title'],
            details=json['details'] if 'details' in json else "",
            checked=json['checked'] if 'checked' in json else False,
            file_path=url
        )
        return make_response(item, OK)
    except IncorrectData as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, {"msg": e.args[0]})
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, {"msg": e.args[0]})


@todo.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id: int):
    current_app.logger.info(f"deleting todo {id}...")
    try:
        item = todo_serice.delete(id)
        return make_response(item, OK)
    except ItemNotExists as e:
        current_app.logger.error(e.args[0])
        return http_response(BAD_REQUEST, {"msg": e.args[0]})


@todo.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
