from flask import Flask
from dotenv import dotenv_values

from api.routes.todo import todo


def create_app() -> Flask:
    config = dotenv_values('.env')
    app = Flask(__name__)
    app.register_blueprint(todo)
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
