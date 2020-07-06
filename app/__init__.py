import os
import re
from flask import Flask, make_response, request, abort
from datetime import datetime
import pymongo

from app.utils.json import JSONParser
from app.utils import middleware, errorHandle
from app.api.home import HomeRoute
from app.api.comic import ComicRoute
from app.api.author import AuthorRoute
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
AuthorRoute(app)
ChapterRoute(app)

# WEB
@app.route("/", methods=['GET'])
def home():
    # client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
    # db = client.vncomics
    # comics = db.comics
    # comics.insert_one({
    #     u'name': 'item',
    #     u'nameNoAccent': 'self.no_accent_vietnamese(item)',
    #     u'cover': 'item',
    #     u'isHot': 'item',
    #     u'url': 'item'
    # })
    # print('---------------------------------------------------------')
    # print(client)
    # print('---------------------------------------------------------')
    # print(db)
    # print('---------------------------------------------------------')
    # print(comics)
    # print('---------------------------------------------------------')
    # print(comics)
    # print('---------------------------------------------------------')
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "Hello, There!" + " It's " + formatted_now
