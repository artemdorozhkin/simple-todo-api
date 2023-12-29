from pathlib import Path


def read_sql(path: Path):
    if not path.suffix.lower() == '.sql':
        raise Exception('file is not sql')
    
    with open(str(path.resolve()), 'r') as file:
        return file.read()
