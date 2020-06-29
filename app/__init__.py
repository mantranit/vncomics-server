import os
import re
from flask import Flask, make_response, request, abort
from datetime import datetime
import pymongo

from app.utils.json import JSONParser
from app.utils import middleware, errorHandle
from app.views.home import HomeRoute
from app.views.comics import ComicsRoute
from app.views.categories import CategoriesRoute

app = Flask(__name__)
middleware(app)
errorHandle(app)

@app.route("/", methods=['GET'])
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "Hello, There!" + " It's " + formatted_now

ComicsRoute(app)
HomeRoute(app)
CategoriesRoute(app)
