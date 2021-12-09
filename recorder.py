import argparse
import socket
import bluetooth
import pika
import pymongo
import pickle
import hashlib
import json
from cryptography.fernet import Fernet
from BGRDetector import get_outcome
from phone_parser import parse_message

def bluetooth_receive(client_sock):
    client_msg = client_sock.recv(1024)
    client_msg_str = client_msg.decode()
    return client_msg_str

def send_to_server(msg):
    key = Fernet.generate_key()
    encryption = Fernet(key)
    encrypted_msg = encryption.encrypt(msg.encode())
    checksum = hashlib.md5(encrypted_msg).hexdigest()
    payload = (key, encrypted_msg, checksum)
    pickled_payload = pickle.dumps(payload)
    sock.send(pickled_payload)
    print("Sent the encrypted information to the server")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-sip', type=str, required=True, help="Server IP Address", metavar="SERVER_IP")
    parser.add_argument('-sp', type=int, required=True, help="Server Port Number", metavar="SERVER_PORT")
    args = parser.parse_args()

    SERVER_IP = args.sip
    SERVER_PORT = args.sp
    SOCKET_SIZE = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print("Connecting to " + str(SERVER_IP) + " on port " + str(SERVER_PORT))

    bluetooth_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM )
    port = 1
    bluetooth_sock.bind(("",port))
    bluetooth_sock.listen(port)
    print("Waiting to accept bluetooth connection")
    client_sock,address = bluetooth_sock.accept()
    print("Successfully established a bluetooth connection with %s", address)
    
    competition_name = bluetooth_receive(client_sock).strip()
    print("Received Competition name: " + competition_name)
    
    while True:

        lifter, lift, attempt, weight = parse_message(bluetooth_receive(client_sock))
        print("Received the following from ", address, lifter, lift, attempt, weight)
        judge = []
        judge, result = get_outcome()
        print("The judge's results are in", judge[0], judge[1], judge[2])
        
        data = {"competition_name": competition_name, "lifter_name" : lifter, "lift_name" : lift, "attempt_number" : attempt, "weight" : weight, "judgements" : judge, "result" : result}
        json_dump = json.dumps(data)
        send_to_server(json_dump)



