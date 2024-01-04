def readsql(path: str):
    with open(path, "r") as sql:
        return sql.read()


def to_dict(description, result):
    columns = [col[0] for col in description]
    if isinstance(result, tuple):
        return dict(zip(columns, result))
    else:
        return [dict(zip(columns, row)) for row in result]
