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
        randomDb = self.comics.aggregate( [ { "$sample": { "size" : 12} }, { "$project": { "_id": 1, "name": 1, "cover": 1 } } ] )  
        latestDb = self.comics.find({},{ "_id": 1, "name": 1, "cover": 1 }).sort("updatedAt", -1).limit(12)
        hotestDb = self.comics.find({ "isHot": True },{ "_id": 1, "name": 1, "cover": 1 }).limit(12)
        completedDb = self.comics.find({ "status": 1 },{ "_id": 1, "name": 1, "cover": 1 }).limit(12)

        completed = list(completedDb)
        if len(completed) == 0:
            completed = list(randomDb)

        tmp = list(latestDb)

        return JSONParser({
            "random": list(randomDb),
            "hotest": list(hotestDb),
            "latest": tmp,
            "completed": completed,
        })

