'''
Class server for running a web server for queries and running a socket connection for input data
Author: Connor Mackert
Date last modified: 7 December, 2021
'''

from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from bson.json_util import dumps as modified_dumps
import requests
import pymongo
import Keys
import pickle
import socket
import threading
import json
import Database

app = Flask(__name__)
auth = HTTPBasicAuth()
db = Database.Database()

SOCKET_SIZE = 1024
PORT = 6000

# View lifter info
@app.route('/view', methods=['GET'])
def view():
    competition_name = request.args.get('competition_name')
    lifter_name = request.args.get('lifter_name')
    search_key = request.args.get('search_key')
    search_value = request.args.get('search_value')
    
    # Check validity
    if competition_name == None:
        return display_help()
    if search_key == None and search_value != None:
        return display_help()
    if search_key != None and search_value == None:
        return display_help()
    
    # Display all competition data
    if lifter_name == None and search_key == None and search_value == None:
        comp_data = db.find(_competition=competition_name)
        return modified_dumps(comp_data)
    
    # Display all lifts for specific lifter
    if search_key == None and search_value == None:
        lifter_data == db.find(_competition=competition_name, _lifter=lifter_name)
        return modified_dumps(lifter_data)
    
    # Search whole competition for query
    if lifter_name == None:
        lifter_data = db.find(_competition=competition_name, query_key=search_key, query_value=search_value)
        return modified_dumps(lifter_data)
    
    # Search specific lifter for query
    lifter_data = db.find(_competition=competition_name, _lifter=lifter_name, query_key=search_key, query_value=search_value)
    return modified_dumps(lifter_data)

def display_help():
    return 'USAGE:\n\nMUST Specify competition_name\nAll lifts for a certain lifter: ?competition_name="competition name"&lifter_name="name"\nLifts for a certain lifter that match criteria: ?competition_name="competition name"&lifter="name"&search_key="search key"&search_value="search value"\nAll lifters in competition that match critera: ?competition_name="competition name"&search_key="search key"&search_value="search value\nAll lifts in competition: ?competition_name="competition name\n\nVALID SEARCH KEYS:\n\nlifter (underscore between fist and last name)\nlift (Squat/Bench/Deadlift)\nattempt_number\nweight ([number]lbs)\nresult (Pass/Fail)'

# Change lifter info
@app.route('/view/change', methods=['POST', 'PUT', 'DELETE'])
@auth.login_required
def change():
    operation = request.args.get('operation')
    lifter_name = request.args.get("lifter_name")
    lift_name = request.args.get("lift_name")
    attempt = request.args.get("request")
    attempt_one = request.args.get("attempt_one")
    attempt_two = request.args.get("attempt_two")
    attempt_three = request.args.get("attempt_three")

    if operation == 'add_lift' or operation == 'update':
        db.add(lifter_name, lift_name, attempt, [judge_one, judge_two, judge_three])

    if operation == 'delete':
        db.delete(lifter_name, lift_name, attempt, outcome)

def connect_to_recorder():
    db = Database.Database()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen()

    recorder, addr = s.accept()
    while True:
        try:
            payload_serialized = client.recv(SOCKET_SIZE)
            payload_json = pickle.loads(payload_serialized)
            payload = json.load(payload_json)

            lifter = payload['lifter']
            lift = payload['lift']
            attempt = payload['attempt']
            attempt_one = payload['attempt_one']
            attempt_two = payload['attempt_two']
            attempt_three = payload['attempt_three']

            db.Insert_one(lifter, lift, attempt, [attempt_one, attempt_two, attempt_three])
            print("Lift recorded")

        except KeyboardInterrupt:
            print('No longer connected to recorder')
            client.close()
            break;

if __name__ == '__main__':
#     socket_thread = threading.Thread(target=connect_to_recorder)
#     socket_thread.start()
#     db = Database.Database()
#     data = {'lifter': 'Connor Mackert', 'lift': 'Squat', 'attempt_number': '1', 'weight': '465lbs', 'judgements': [True, True, False]}
#     db.add("USPA_Nationals", "Connor_Mackert", data)
    app.run(host='0.0.0.0', debug=True)
