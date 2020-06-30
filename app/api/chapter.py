from app.models import Models
from app.utils.json import JSONParser
from bson import ObjectId

def ChapterRoute(app):

    @app.route("/api/chapters/<id>", methods=['GET'])
    def api_chapters(id):
        return ChapterAPI().CtrlGetById(id)

    pass

class ChapterAPI:
    def __init__(self):
        model = Models()
        self.chapters = model.chapters
    
    def CtrlGetById(self, id):
        row = self.chapters.find_one({ "_id": ObjectId(id) })

        return JSONParser(row)
