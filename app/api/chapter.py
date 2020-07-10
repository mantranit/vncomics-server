from app.models import Models
from app.utils.json import JSONParser
from bson import ObjectId
import boto3
from boto3.dynamodb.types import TypeDeserializer
from flask import abort

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

        dynamodb = boto3.resource('dynamodb')
        chapters = dynamodb.Table('chapters')

        row = chapters.get_item(
            Key={
                'id': id
            }
        )

        print('-----------------')
        print(row)

        # row = self.dynamodb.get_item(
        #     TableName='chapters',
        #     Key={
        #         'id': {
        #             'S': id
        #         }
        #     }
        # )
        
        if 'Item' in row:
            # deserializer = TypeDeserializer()
            # data = {k: deserializer.deserialize(v) for k,v in row['Item'].items()}
            data = row['Item']

            return JSONParser(data)
        
        return abort(404, id)
