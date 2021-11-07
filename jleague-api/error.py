from flask import Response
import json

def response_error(message, status):
    return Response(response=json.dumps({"message":message}, ensure_ascii=False, indent=4), status=status)