from app.models import Models
from app.utils.json import JSONParser
from bson import ObjectId

def ComicsRoute(app):

    @app.route("/api/comics", methods=['POST'])
    def api_comics():
        return ComicsAPI().CtrlGetAll()

    @app.route("/api/comics/<id>", methods=['GET'])
    def api_comicById(id):
        return ComicsAPI().CtrlGetById(id)

    pass

class ComicsAPI:
    def __init__(self):
        model = Models()
        self.comics = model.comics
    
    def CtrlGetAll(self):
        rows = self.comics.aggregate([
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
                "$project": {
                    "name": "$name",
                    "cover": "$cover"
                }
            },
            { "$limit": 10 }
        ])

        tmp = list(rows)

        return JSONParser({
            "random": tmp,
            "hotest": tmp,
            "latest": tmp,
            "completed": tmp,
        })

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

