import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import dotenv_values
from flasgger import Swagger

from api.routes import routes

config = dotenv_values('.env')


def create_app() -> Flask:
    app = Flask(__name__)
    (app.register_blueprint(route) for route in routes)

    JWTManager(app)
    app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']

    app.config['SWAGGER'] = {
        'doc_dir': './specs/'
    }
    Swagger(app, parse=True, template_file=os.path.join(
        os.getcwd(), "specs", "definitions.yaml")
    )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=config['APP_HOST'],
        port=config['APP_PORT'],
        debug=config['APP_DEBUG']
    )
