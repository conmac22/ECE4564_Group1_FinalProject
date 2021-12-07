'''
Class Database for entering and retrieving information from MongoDB
Author: Sean Quiterio
Date last modified: 30 November, 2021
'''

import DatabaseKeys
import pymongo
import time

class Database:
    def __init__(self):
        # Import Keys to connect to MongoDB Atlas
        username = DatabaseKeys.username
        mongoPassword = DatabaseKeys.pw

        # Connect to mongoDB
        self.cluster = pymongo.MongoClient(
            'mongodb+srv://' + username + ':' + mongoPassword + '@cluster0.kvaed.mongodb.net/Cluster0?retryWrites=true&w=majority')

    def Insert_one(self, warehouse, _collection, attempt, outcome):
        # Insert a lift into the database
        db = self.cluster[warehouse]
        collection = db[_collection]
        MsgID = "1$" + str(time.time())
        Lifter = warehouse
        Lift = _collection

        if attempt < 0 or attempt > 3:
            return False
        elif len(outcome) == 3:
            total = 0
            for result in outcome:
                total += result
                if total < 2:
                    overall = "Fail"
                else:
                    overall = "Pass"
        else:
            return False

        document = {"MsgID":MsgID, "Lifter":Lifter, "Lift":Lift, "Attempt":attempt, "Outcome":outcome, "Overall":overall}
        collection.insert_one(document)

        return True

    def Find_all(self, warehouse, _collection=None, _attempt=None):
        db = self.cluster[warehouse]
        posts = []
        if _collection == None:
            for post in db.find():
                posts.append(post)
            return posts
        elif _attempt == None:
            collection = db[_collection]
            posts = []
            for post in collection.find():
                posts.append(post)
            return posts
        collection = db[_collection]
        return collection.find_one({"Attempt":_attempt})

    def Delete_Many(self, warehouse, _collection=None, _attempt=None, query):
        db = self.cluster[warehouse]
        if _collection == None:
            return db.deleteMany(query)
        collection = db[_collection]
        return collection.deleteMany(query)
