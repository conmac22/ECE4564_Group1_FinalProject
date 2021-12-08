'''
Class Database for entering and retrieving information from MongoDB
Author: Sean Quiterio
Date last modified: 7 December, 2021
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

    # Add
    def add(self, _competition, _lifter, data):
        competition = self.cluster[_competition]
        lifter = competition[_lifter]
        msgID = '1$' + str(time.time())

        if data['attempt_number'] < 0 or data['attempt_number'] > 3:
            return False
        total = 0
        result = 'Error'
        for judgement in data['judgements']:
            if judgement:
                total += 1
        if total < 2:
            result = 'Fail'
        elif total != 'Error':
            result = 'Pass'
        else:
            return False

        document = {'MsgID': msgID, 'lifter': data['lifter'], 'lift': data['lift'], 'attempt_number': data['attempt_number'], 'weight': data['weight'], 'judgements': data['judgements'], 'result': result}
        lifter.insert_one(document)

        return True

    # View
    def find(self, _competition, _lifter=None, query_key=None, query_value=None):
        competition = self.cluster[_competition]
        
        matches = []
        
        # Search through all lifters
        if _lifter == None:
            for lifter in competition.getCollectionNames():
                for match in competition[lifter].find({query_key: query_value}):
                    matches.append(match)
                return matches
        # Search through specific lifter
        lifter = competition[_lifter]
        for match in lifter.find({query_key: query_value}):
            matches.append(match)
        return matches

    # Delete
    def delete(self, _competition, _lifter=None, query_key=None, query_value=None):
        competition = self.cluster[_competition]
        lifter = competition[_lifter]
        
        if query_key == 'clear_lifter':
            return competition[lifter].drop()
        
        return lifter.deleteMany()
        
        
            
        db = self.cluster[warehouse]
        if _collection == None:
            return db.deleteMany(query)
        collection = db[_collection]
        return collection.deleteMany({query_key: query_value})