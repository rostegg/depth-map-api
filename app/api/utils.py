from flask import Response
import json

def response(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=json.dumps(data)
    )