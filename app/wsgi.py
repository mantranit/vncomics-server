import flask
from flask import make_response, request, jsonify
from datetime import datetime
import re
import json
from bson import ObjectId
import pymongo

import middleware

app = flask.Flask(__name__)
app.wsgi_app = middleware.Middleware(app.wsgi_app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

@app.after_request
def after_request_func(data):
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route("/", methods=['GET'])
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "Hello, There!" + " It's " + formatted_now

@app.route("/comics", methods=['GET'])
def comics():
    client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
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
    return json.dumps({"data": list(rows)}, ensure_ascii=False, cls=JSONEncoder)

@app.route("/hello/<name>", methods=['GET'])
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return jsonify({ "data": content})
