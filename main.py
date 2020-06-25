import falcon
import json
import pymongo
import datetime
import bson.objectid

class TestResource(object):

    def my_handler(self, x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        elif isinstance(x, bson.objectid.ObjectId):
            return str(x)
        else:
            raise TypeError(x)

    def on_get(self, req, res):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.row = self.comics.find_one()

        """Handles all GET requests."""
        res.status = falcon.HTTP_200  # This is the default status
        res.body = json.dumps(self.row, default=self.my_handler)

# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/comics', test_resource)