import falcon
import json
import pymongo
from bson.json_util import dumps

class TestResource(object):
    def on_get(self, req, res):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.category = self.db.categories
        self.authors = self.db.authors
        self.chapters = self.db.chapters
        self.row = self.comics.find_one()

        """Handles all GET requests."""
        res.status = falcon.HTTP_200  # This is the default status
        res.body = dumps(self.row)

# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/', test_resource)