from os import path
from typing import Callable
from flask import Request


def readsql(path: str):
    with open(path, "r") as sql:
        return sql.read()


def to_dict(description, result):
    columns = [col[0] for col in description]
    if isinstance(result, tuple):
        return dict(zip(columns, result))
    else:
        return [dict(zip(columns, row)) for row in result]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [
               'jpg', 'jpeg', 'png', 'bmp', 'gif'
           ]


def generate_unique_filename(filename: str):
    _, ext = path.splitext(filename)

    from uuid import uuid4
    unique_filename = str(uuid4()) + ext
    return unique_filename


def save_file(files, folder):
    filename = ''
    if files:
        file = files['image']
        if allowed_file(file.filename):
            filename = generate_unique_filename(file.filename)
            file_path = path.join(
                folder, filename
            )
            file.save(file_path)
    return filename
