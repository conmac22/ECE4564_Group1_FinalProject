from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import requests
import pymongo
import Keys
import pickle
import socket
import threading

app = Flask(__name__)
auth = HTTPBasicAuth()

# View lifter info
@app.route('/view/lifter', methods=['GET'])
def view_lifter():
    lifter_name = request.args.get('lifter_name')
    # Connect to MongoDB
    mongo_assword = Keys.mongo_db_password
    cluster = pymongo.MongoClient('mongodb+srv://seans_laptop:' + mongoPassword + '@cluster0.kvaed.mongodb.net/Cluster0?retryWrites=true&w=majority')
    db = cluster["ECE4564_Final_Project"]
    collection = db["competition_data"]
    
# View lift info
@app.route('/view/lift', methods=['GET'])
def view_lifter():
    lift_name = request.args.get('lift_name')
    # Connect to MongoDB
    mongo_assword = Keys.mongo_db_password
    cluster = pymongo.MongoClient('mongodb+srv://seans_laptop:' + mongoPassword + '@cluster0.kvaed.mongodb.net/Cluster0?retryWrites=true&w=majority')
    db = cluster["ECE4564_Final_Project"]
    collection = db["competition_data"]
    
    if lift == 'squat':
        i = 0 #Placeholder
        
    if lift == 'bench':
        i = 0 #Placeholder
        
    if lift == 'deadlift':
        i = 0 #Placeholder
        
# Change meet info
@app.route('/view/lifter', methods=['POST', 'PUT', 'DELETE'])
@auth.login_required
def change_info():
    operation = request.args.get('operation')
    # Connect to MongoDB
    mongo_assword = Keys.mongo_db_password
    cluster = pymongo.MongoClient('mongodb+srv://seans_laptop:' + mongoPassword + '@cluster0.kvaed.mongodb.net/Cluster0?retryWrites=true&w=majority')
    db = cluster["ECE4564_Final_Project"]
    collection = db["competition_data"]
    
    if operation == 'add':
        i = 0 #Placeholder
        
    if operation == 'update':
        i = 0 #Placeholder
        
    if operation == 'delete':
        i = 0 #Placeholder
        
def connect_to_recorder():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,SERVER_PORT))
    s.listen()
    
    recorder, addr = s.accept()
    while True:
        try:
            i = 0 # Placehlder
            # Deserialize recorder data
            # Store in mongoDB
        except KeyboardInterrupt:
            print('No longer connected to recorder')
            client.close()
            break;
            
    

if __name__ == '__main__':
    socket_thread = threading.Thread(target=connect_to_recorder)
    socket_thread.start()
    app.run(host='0.0.0.0')