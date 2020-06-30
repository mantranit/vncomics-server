import os
import re
from flask import Flask, make_response, request, abort
from datetime import datetime
import pymongo

from app.utils.json import JSONParser
from app.utils import middleware, errorHandle
from app.api.home import HomeRoute
from app.api.comic import ComicRoute
from app.api.category import CategoryRoute
from app.api.chapter import ChapterRoute

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
middleware(app)
errorHandle(app)

# API
HomeRoute(app)
ComicRoute(app)
CategoryRoute(app)
ChapterRoute(app)

# WEB
@app.route("/", methods=['GET'])
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "Hello, There!" + " It's " + formatted_now
