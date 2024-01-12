import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import dotenv_values

from api.routes import routes

config = dotenv_values('.env')


def create_app() -> Flask:
    app = Flask(__name__)
    for route in routes:
        app.register_blueprint(route)

    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.getcwd(), "public", "uploads"
    )

    JWTManager(app)
    app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']

    app.config['SWAGGER'] = {
        'title': 'TODO API DOCS',
        'doc_dir': './specs/'
    }
    def_path = os.path.join(os.getcwd(), "specs", "definitions.yml")
    Swagger(app, template_file=def_path, parse=True)

    return app


if __name__ == "__main__":
    app = create_app()
    if config['PRODUCTION'].lower() == "true":
        print("server running in production mode")
        from waitress import serve
        serve(
            app,
            host=config['APP_HOST'],
            port=config['APP_PORT']
        )
    else:
        app.run(
            host=config['APP_HOST'],
            port=config['APP_PORT'],
            debug=config['APP_DEBUG']
        )
