# TODO API

[original task](TODO_API.md)

edit .env file

```bash
git clone https://github.com/artemdorozhkin/lesson-01-simple-todo-api.git
```

```bash
docker compose -f ./docker/docker-compose.yml build
docker compose -f ./docker/docker-compose.yml up
```

or in detach mode:

```bash
docker compose -f ./docker/docker-compose.yml build
docker compose -f ./docker/docker-compose.yml up -d
```

### or for older docker version:

```bash
docker-compose -f ./docker/docker-compose.yml build
docker-compose -f ./docker/docker-compose.yml up
```

or in detach mode:

```bash
docker-compose -f ./docker/docker-compose.yml build
docker-compose -f ./docker/docker-compose.yml up -d
```

## DOCS

open browser with url:

```url
http://127.0.0.1/apidocs
```
