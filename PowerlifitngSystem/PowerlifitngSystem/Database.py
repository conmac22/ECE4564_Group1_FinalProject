'''
Class Database for entering and retrieving information from MongoDB
Author: Sean Quiterio
Date last modified: 7 December, 2021
'''

import DatabaseKeys
import pymongo
from bson.objectid import ObjectId

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

        document = {'lifter_name': data['lifter_name'], 'lift': data['lift_name'], 'attempt_number': data['attempt_number'], 'weight': data['weight'], 'judgements': data['judgements'], 'result': data['result']}
        return lifter.insert_one(document)

    # View
    def find(self, _competition, _lifter=None, query_key=None, query_value=None):
        competition = self.cluster[_competition]
        
        matches = []
        
        # Display all competition data
        if _lifter == None and query_key == None and query_value == None:
            for lifter in competition.collection_names():
                for lift in competition[lifter].find():
                    matches.append(lift)
                return matches
            
        # Display all lifts for specific lifter
        if query_key == None and query_value == None:
            lifter = competition[_lifter]
            for lift in lifter.find():
                matches.append(lift)
            return matches
            
        
        # Search whole competition for query
        if _lifter == None and query_key != None and query_value != None:
            for lifter in competition.collection_names():
                for lift in competition[lifter].find({query_key: query_value}):
                    matches.append(lift)
                return matches
            
        # Search specific lifter for query
        lifter = competition[_lifter]
        for lift in lifter.find({query_key: query_value}):
            matches.append(lift)
        return matches
    
    # Update
    def update(self, _competition, _lifter, _id, key, value):
        competition = self.cluster[_competition]
        lifter = competition[_lifter]
        if lifter.find_one({'_id': ObjectId(_id)}) == None:
            return 'Could not find document with specified ID'
        return lifter.update_one(lifter.find_one({'_id': ObjectId(_id)}), {'$set': {key: value}})
        

    # Delete
    def delete(self, _competition, _lifter=None, query_key=None, query_value=None):
        competition = self.cluster[_competition]
        
        # Delete by query in all competitions
        if _lifter == None:
            for lifter in competition.collection_names():
                return lifter.delete_many({query_key: query_value})

        lifter = competition[_lifter]
            
        # Delete lifter
        if query_key == None and query_value == None:
            lifter.drop()
            return _lifter
        
        # Delete by query for specific lifter
        return lifter.delete_many({query_key: query_value})
