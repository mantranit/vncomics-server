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
        randomDb = self.comics.aggregate( [ { "$sample": { "size" : 12} }, { "$project": { "_id": 1, "name": 1, "cover": 1, "url": 1 } } ] )  
        latestDb = self.comics.find({},{ "_id": 1, "name": 1, "cover": 1, "url": 1 }).sort("updatedAt", -1).limit(12)
        hotestDb = self.comics.find({ "isHot": True },{ "_id": 1, "name": 1, "cover": 1, "url": 1 }).limit(12)
        completedDb = self.comics.find({ "status": 1 },{ "_id": 1, "name": 1, "cover": 1, "url": 1 }).limit(12)

        random = list(randomDb)
        completed = list(completedDb)
        if len(completed) == 0:
            completed = random

        tmp = list(latestDb)

        return JSONParser({
            "random": random,
            "hotest": list(hotestDb),
            "latest": tmp,
            "completed": completed,
        })

