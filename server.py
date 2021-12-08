'''
Class server for running a web server for queries and running a socket connection for input data
Author: Connor Mackert
Date last modified: 7 December, 2021
'''

from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
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

    # Search whole competition
    if lifter_name == '':
        lifter_data = db.find(_competition=competition_name, query_key=search_key, query_value=search_value)
        return jsonify({'result': lifter_data})
    # Search specific lifter
    lifter_data = db.find(_competition=competition_name, _lifter=lifter_name, query_key=search_key, query_value=search_value)
    return lift_data

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
        db.Insert_one(lifter_name, lift_name, attempt, [judge_one, judge_two, judge_three])

    if operation == 'delete':
        db.Delete_many(lifter_name, lift_name, attempt, outcome)

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
    db = Database.Database()
    data = {'lifter': 'Connor Mackert', 'lift': 'Squat', 'attempt_number': 1, 'weight': '465 lbs', 'judgements': [True, True, False]}
    db.add("USPA_Nationals", "Connor_Mackert", data)
    #app.run(host='0.0.0.0', debug=True)
