from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import dotenv_values

from api.routes.todo import todo
from api.routes.auth import auth


def create_app() -> Flask:
    config = dotenv_values('.env')
    app = Flask(__name__)
    jwt = JWTManager(app)
    app.register_blueprint(todo)
    app.register_blueprint(auth)
    app.config['JWT_SECRET_KEY'] = config['SECRET_KEY']

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
