from app.models import Models
from app.utils.json import JSONParser
from bson import ObjectId

def HomeRoute(app):

    @app.route("/api/home", methods=['GET'])
    def api_home():
        return HomeAPI().CtrlGet()

    pass

class HomeAPI:
    def __init__(self):
        model = Models()
        self.comics = model.comics
    
    def CtrlGet(self):
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
            { "$limit": 12 }
        ])

        tmp = list(rows)

        return JSONParser({
            "random": tmp,
            "hotest": tmp,
            "latest": tmp,
            "completed": tmp,
        })

