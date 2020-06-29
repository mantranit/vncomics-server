import os
import re
from flask import make_response, request, abort, jsonify

def middleware(app):
    @app.before_request
    def before_request_func():
        matchApi = re.match("^/api/.*", request.path)
        if matchApi:
            apiKey = request.headers.get('x-api-key')
            if not apiKey or apiKey != os.getenv('X_API_KEY'):
                abort(403, description="Missing x-api-key or the x-api-key is NOT match")

    @app.after_request
    def after_request_func(data):
        response = make_response(data)
        matchApi = re.match("^/api/.*", request.path)
        if matchApi:
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

def errorHandle(app):

    def errorResponse(e, code):
        matchApi = re.match("^/api/.*", request.path)
        if matchApi:
            return jsonify(error=str(e)), code
        else:
            return str(e), code

    @app.errorhandler(401)
    def resource_unauthorized(e):
        return errorResponse(e, 401)

    @app.errorhandler(403)
    def resource_forbidden(e):
        return errorResponse(e, 403)

    @app.errorhandler(404)
    def resource_not_found(e):
        return errorResponse(e, 404)

    @app.errorhandler(405)
    def resource_not_allowed(e):
        return errorResponse(e, 405)

    @app.errorhandler(500)
    def resource_internal_error(e):
        return errorResponse(e, 500)