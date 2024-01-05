from flask import jsonify, make_response


def http_response(code, text):
    return make_response(
        jsonify(code=code, **text),
        code
    )
