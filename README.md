# TODO API

[original task](TODO_API.md)

is a simple api for creating, editing and deleting TODOs. api supports user authentication.

## Get started

Clone the repository:

```powershell
git clone https://github.com/artemdorozhkin/lesson-01-simple-todo-api.git
```

Edit the .env.sample file and rename it to .env.
For a production mode, set `PRODUCTION = True`.

Create a virtual environment:

```powershell
python -m venv venv
```

and install the dependencies:

```powershell
pip install -r .\requirements.txt
```

To run in docker, use the following command:

```powershell
.\api.bat docker build
.\api.bat docker up -d
```

to stop the application, run:

```powershell
.\api.bat docker down
```

To run the application without the docker, run the following command:

```powershell
.\api.bat run
```

The application will be available on the specified host and port in the .env file

## DOCS

To view the documentation, please go to url:

```url
http://${APP_HOST}:${APP_PORT}/apidocs
```
