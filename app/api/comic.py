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


    @app.route("/api/countdown", methods=['GET'])
    def api_countdown():
        return ComicAPI().CtrlCountDown()

    @app.route("/api/reset-db", methods=['POST'])
    def api_reset_db():
        return ComicAPI().CtrlResetDB()

    pass

class ComicAPI:
    def __init__(self):
        model = Models()
        self.comics = model.comics
    
    def CtrlGetAll(self, parameters):
        stages = [
            { 
                "$lookup": {
                    "from": "categories", 
                    "localField": "categories", 
                    "foreignField": "_id",
                    "as": "categories"
                }
            }
        ]

        text = parameters.get("text")
        if text:
            rgx = re.compile(u'.*' + text + '.*', re.IGNORECASE)  # compile the regex
            stages.append({ 
                '$match': { "$or": [ {"name": rgx}, {"nameNoAccent": rgx}, {"body": rgx} ] }
            })

        category = parameters.get("category")
        if category:
            stages.append({
                "$match": { "categories": ObjectId(category) }
            })

        author = parameters.get("author")
        if author:
            stages.append({
                "$match": { "authors": ObjectId(author) }
            })

        total = 0
        stage_count = list(stages)
        stage_count.append({ "$count": "myCount" })
        resultCount = self.comics.aggregate(stage_count)
        resultCount = list(resultCount)
        if resultCount:
            total = resultCount[0]["myCount"]

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

        stages.append({
            "$project": {
                "nameNoAccent": 0,
                "chapters": 0,
                "authors": 0,
                "url": 0,
                "body": 0,
                "createdAt": 0,
                "altName": 0,
                "referer": 0,
                "crawled": 0
            }
        })

        rows = self.comics.aggregate(stages)
        
        return JSONParser({
            "list": list(rows),
            "total": total,
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
                "$project": {
                    'nameNoAccent': 0,
                    "url": 0,
                    "referer": 0,
                    "crawled": 0
                }
            }
        ])

        if rows.alive:
            return JSONParser(list(rows)[0])
        return JSONParser(None)
        pass

    def CtrlCountDown(self):
        remain = self.comics.count({"crawled": {"$exists": False}})
        total = self.comics.count()
        return { "total": total, "remain": remain, "percent": round(((total - remain)/total) * 100, 2) }
        pass

    def CtrlResetDB(self):
        self.comics.update_many(
            { 
                "crawled": True 
            }, {
                "$set": { "crawled": False }
            })

        return JSONParser(None)
        pass

