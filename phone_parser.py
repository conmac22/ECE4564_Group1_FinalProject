'''
Methods for parsing messages from a mobile phone
Author: Sean Quiterio
Date last modified: 9 December, 2021
'''

# Example competition message: "Competition: <Name>"
# Example message: "Lifter: <Name>, Lift: <Lift>, Attempt: <number>, Weight: <lbs>"

def parse_message(message):
    message = message.strip()
    message_params = message.split(',')
    print("message params: " + str(message_params))
    lifter = message_params[0].split(' ')[1]
    lift = message_params[1].split(' ')[2]
    attempt = message_params[2].split(' ')[2]
    weight = message_params[3].split(' ')[2]
    return lifter, lift, attempt, weight

if __name__ == "__main__":
    message = "Lifter: balls, Lift: Bench, Attempt: 1, Weight: 405"
    lifter, lift, attempt, weight = parse_message(message)
    print("lifter: " + lifter)
    print("lift: " + lift)
    print("attempt: " + attempt)
    print("weight: " + weight)
