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
        self.dynamodb = model.dynamodb
    
    def CtrlGetById(self, id):
        row = self.dynamodb.get_item(
            TableName='chapters',
            Key={
                'id': {
                    'S': id
                }
            }
        )

        return JSONParser(row)
