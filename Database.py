'''
Class Database for entering and retrieving information from MongoDB
Author: Sean Quiterio
Date last modified: 7 December, 2021
'''

import DatabaseKeys
import pymongo

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

        document = {'lifter': data['lifter'], 'lift': data['lift'], 'attempt_number': data['attempt_number'], 'weight': data['weight'], 'judgements': data['judgements'], 'result': result}
        lifter.insert_one(document)

        return True

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
        print({query_key: query_value})
        for lift in lifter.find({query_key: query_value}):
            matches.append(lift)
        return matches

    # Delete
    def delete(self, _competition, _lifter=None, query_key=None, query_value=None):
        competition = self.cluster[_competition]
        lifter = competition[_lifter]
        
        if query_key == 'clear_lifter':
            return competition[lifter].drop()
        
        return lifter.deleteMany()