import os
import pymongo

class Models:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('DATABASE_URI'))
        self.db = self.client.vncomics
        self.authors = self.db.authors
        self.categories = self.db.categories
        self.chapters = self.db.chapters
        self.comics = self.db.comics
        