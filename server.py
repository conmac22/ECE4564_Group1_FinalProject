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
db = Database()

SOCKET_SIZE = 1024
PORT = 5000

# View lifter info
@app.route('/view', methods=['GET'])
def view():
    lifter_name = request.args.get('lifter_name')
    lift_name = request.args.get('lift_name')

    # Lifter data only
    if lift_name == '':
        lifter_data = db.Find_all(lifter_name)
        return lifter_data
    # Lifter data + lift data
    lift_data = db.Find_all(lifter_name, lift_name)
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
    db = Database()
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
    socket_thread = threading.Thread(target=connect_to_recorder)
    socket_thread.start()
    #app.run(host='0.0.0.0')
