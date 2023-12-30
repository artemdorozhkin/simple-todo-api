from flask import Flask
from api.routes.todo import todo


app = Flask(__name__)
app.register_blueprint(todo)


if __name__ == "__main__":
    app.run(debug=True)
