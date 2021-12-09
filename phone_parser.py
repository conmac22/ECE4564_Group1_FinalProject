'''
Methods for parsing messages from a mobile phone
Author: Sean Quiterio
Date last modified: 9 December, 2021
'''

# Example competition message: "Competition: <Name>"
# Example message: "Lifter: <Name>, Lift: <Lift>, Attempt: <number>"

def parse_message(message):
    message = message.trim()
    message_params = message.split(',')
    lifter = message_params[0].split(' ')[1]
    lift = message_params[1].split(' ')[1]
    attempt = message_params[2].split(' ')[1]
    return lifter, lift, int(attempt)

def parse_competition(message):
    message = message.trim()
    comp = message.spli(' ')
    return comp[1]
