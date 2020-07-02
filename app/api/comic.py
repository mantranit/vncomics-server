import re
from flask import request, current_app as app
from app.models import Models
from app.utils.json import JSONParser
from bson import ObjectId

def ComicRoute(app):

    @app.route("/api/comics", methods=['GET'])
    def api_comics():
        return ComicAPI().CtrlGetAll(request.args)

    @app.route("/api/comics/<id>", methods=['GET'])
    def api_comicById(id):
        return ComicAPI().CtrlGetById(id)

    pass

class ComicAPI:
    def __init__(self):
        model = Models()
        self.comics = model.comics
    
    def CtrlGetAll(self, parameters):
        stages = []

        text = parameters.get("text")
        if text:
            rgx = re.compile(u'.*' + text + '.*', re.IGNORECASE)  # compile the regex
            stages.append({ 
                "$name": rgx
            })

        category = parameters.get("category")
        if category:
            stages.append({
                "$match": { "categories": ObjectId(category) }
            })

        # stage_count = list(stages)
        # stage_count.append({ "$count": "myCount" })
        # total = self.comics.aggregate(stage_count)
        # total = list(total)[0]["myCount"]

        sort = parameters.get("sort")
        if sort:
            if sort[0] == "-":
                stages.append({ "$sort": { sort.strip("-"): -1 } })
            else:
                stages.append({ "$sort": { sort: 1 } })

        skip = parameters.get("skip")
        if not skip:
            skip = 0
        stages.append({ "$skip": int(skip) })

        limit = parameters.get("limit")
        if not limit:
            limit = app.config["PAGE_SIZE_DEFAULT"]
        stages.append({ "$limit": int(limit) })

        # stages.append({
        #     "$unset": [
        #         'chapters',
        #         "categories",
        #         "authors",
        #         "url",
        #         "body",
        #         "createdAt"
        #     ]
        # })

        # rows = self.comics.aggregate(stages)
        print('---------------------------------------')
        print(self.comics)
        print('---------------------------------------')
        rgx = re.compile(u'.*' + text + '.*', re.IGNORECASE)  # compile the regex
        rows = self.comics.find({ "$or": [ {"name": rgx}, {"body": rgx} ] }).limit(limit)
        return JSONParser({
            "list": list(rows),
            # "total": total,
            "skip": int(skip),
            "limit": int(limit)
        })
        pass

    def CtrlGetById(self, id):
        rows = self.comics.aggregate([
            {
                "$match": { "_id": ObjectId(id) }
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
                    "from": "categories", 
                    "localField": "categories", 
                    "foreignField": "_id",
                    "as": "categories"
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
            {
                "$unset": [
                    'chapters.comicId', 'chapters.url', 'chapters.pages',
                    "categories.url",
                    "url"
                ]
            }
        ])

        if rows.alive:
            return JSONParser(list(rows)[0])
        return JSONParser(None)
        pass

