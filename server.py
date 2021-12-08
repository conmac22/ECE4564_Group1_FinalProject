'''
Class server for running a web server for queries and running a socket connection for input data
Author: Connor Mackert
Date last modified: 8 December, 2021
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
        return display_help_view()
    if search_key == None and search_value != None:
        return display_help_view()
    if search_key != None and search_value == None:
        return display_help_view()
    
    # Display all competition data
    if lifter_name == None and search_key == None and search_value == None:
        comp_data = db.find(_competition=competition_name)
        return modified_dumps(comp_data)
    
    # Display all lifts for specific lifter
    if search_key == None and search_value == None:
        lifter_data = db.find(_competition=competition_name, _lifter=lifter_name)
        return modified_dumps(lifter_data)
    
    # Search whole competition for query
    if lifter_name == None:
        lifter_data = db.find(_competition=competition_name, query_key=search_key, query_value=search_value)
        return modified_dumps(lifter_data)
    
    # Search specific lifter for query
    lifter_data = db.find(_competition=competition_name, _lifter=lifter_name, query_key=search_key, query_value=search_value)
    return modified_dumps(lifter_data)

# Add lifter data
@app.route('/add', methods=['GET'])
@auth.login_required
def add():  
    # All possible document data 
    competition_name = request.args.get('competition_name')
    lifter_name = request.args.get('lifter_name')
    lift_name = request.args.get('lift_name')
    attempt_number = request.args.get('attempt_number')
    weight = request.args.get('weight')
    judgement_one = str_to_bool(request.args.get('judgement_one'))
    judgement_two = str_to_bool(request.args.get('judgement_two'))
    judgement_three = str_to_bool(request.args.get('judgement_three'))
    result = request.args.get('result')
    
    
    # Error checking
    if competition_name == None:
        return display_help_add()
    if len(request.args) != 9:
        return 'Specify all 9 document fields to add data'
    
    judgements = [judgement_one, judgement_two, judgement_three]
    data = {'lifter': lifter_name, 'lift': lift_name, 'attempt_number': attempt_number, 'weight': weight, 'judgements': judgements, 'result': result}
    return jsonify({'Added': db.add(competition_name, lifter_name, data).acknowledged})
    
# Modify lifter data
@app.route('/update', methods=['GET'])
@auth.login_required
def update():
    competition_name = request.args.get('competition_name')
    lifter_name = request.args.get('lifter_name')
    _id = request.args.get('id')
    key = request.args.get('key')
    value = request.args.get('value')
    
    if competition_name == None:
        return display_help_update()
    if lifter_name == None or key == None or value == None:
        return display_help_update()
    if key == lifter_name:
        return 'Cannot update name. Try deleting and adding instead.'
    
    return jsonify({'Updated': db.update(competition_name, lifter_name, _id, key, value).acknowledged})
    
# Delete lifter data
@app.route('/delete', methods=['GET'])
@auth.login_required
def delete():
    competition_name = request.args.get('competition_name')
    lifter_name = request.args.get('lifter_name')
    search_key = request.args.get('search_key')
    search_value = request.args.get('search_value')
    
    if competition_name == None:
        return display_help_delete()    
    if lifter_name == None and search_key == None and search_value == None:
        return display_help_delete()            
    if search_key == None and search_value != None:
        return display_help_delete()
    if search_key != None and search_value == None:
        return display_help_delete()
    
    if search_key == None and search_value == None:
        return jsonify({'Deleted': db.delete(competition_name, lifter_name, search_key, search_value)})
    return jsonify({'Deleted': db.delete(competition_name, lifter_name, search_key, search_value).acknowledged})

def display_help_view():
    return 'USAGE (Must specify competition name)\n\nAll lifts in competition: curl "http://[server ip]:[5000]/view?competition_name=[competition name]"\nAll lifters in competition that match critera: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&search_key=[search key]&search_value=[search value]"\nAll lifts for a certain lifter: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&lifter_name=[lifter name]"\nAll lifts for a certain lifter that match criteria: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&lifter=[lifter name]&search_key=[search key]&search_value=[search value]"\n\nVALID SEARCH KEYS:\n\nlifter [firstname]_[lastname]\nlift (Squat/Bench/Deadlift)\nattempt_number (1-3)\nweight ([number]lbs)\nresult (Pass/Fail)'        
def display_help_add():
    return 'USAGE\n\ncurl -u user:pass "http://[server_ip]:[5000]/add?competition_name=[competition name]&lifter_name=[lifter name]&lift_name=[lift name]&attempt_number=[attempt number]&weight=[weight]&judgememt_one=[judgement one]&judgememt_two=[judgement two]&judgememt_three=[judgement three]&result=[result]"'
def display_help_update():
    return 'USAGE\n\ncurl -u user:pass "http://[server_ip]:[5000]/update?competition_name=[competition name]&lifter_name=[lifter name]&id=[document id]key=[key]&value=[value]"\n'
def display_help_delete():
    return 'USAGE\n\ncurl -u user:pass "http://[server_ip]:[5000]/delete?competition_name=[competition name]&lifter_name=[lifter name]&search_key=[search key]&search_value=[search value]"\n'

def str_to_bool(string):
    if string == 'True':
        return True
    return False
        
# Authentication
@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'secret':
        return username
    return None

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
    app.run(host='0.0.0.0', debug=True)
