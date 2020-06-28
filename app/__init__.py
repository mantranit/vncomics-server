import flask
from flask import make_response, request, abort, jsonify
from datetime import datetime
import pymongo
import os
import re

from app.utils.json import JSONParser

app = flask.Flask(__name__)

@app.errorhandler(403)
def resource_not_found(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

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

@app.route("/", methods=['GET'])
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "Hello, There!" + " It's " + formatted_now

@app.route("/api/comics", methods=['GET'])
def comics():
    client = pymongo.MongoClient(os.getenv('DATABASE_URI'))
    db = client.vncomics
    comics = db.comics
    rows = comics.aggregate([
        { 
            "$lookup": {
                "from": "categories", 
                "localField": "categories", 
                "foreignField": "_id",
                "as": "categories"
            }
        },
        { 
            "$lookup": {
                "from": "authors", 
                "localField": "authors", 
                "foreignField": "_id",
                "as": "authors"
            }
        },
        { 
            "$lookup": {
                "from": "chapters", 
                "localField": "chapters", 
                "foreignField": "_id",
                "as": "chapters"
            }
        },
        { "$limit": 5 }
    ])
    return JSONParser(list(rows))
