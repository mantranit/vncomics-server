import json
from datetime import datetime
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

def JSONParser(data):
    return json.dumps({
        "statusCode": 200, 
        "message": "Success", 
        "data": data
    }, ensure_ascii=False, cls=JSONEncoder)