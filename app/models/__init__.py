import os
import pymongo
import boto3

class Models:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('DATABASE_URI'))
        self.db = self.client.vncomics
        self.authors = self.db.authors
        self.categories = self.db.categories
        # self.chapters = self.db.chapters      # move to dynamodb
        self.comics = self.db.comics

        self.dynamodb = boto3.client('dynamodb')

        pass
        