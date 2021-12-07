'''
Acquired from: https://www.geeksforgeeks.org/detect-the-rgb-color-from-a-webcam-using-python-opencv/
and: https://maker.pro/raspberry-pi/tutorial/using-opencv-and-raspberry-pi-to-visualize-images-in-different-color-spaces
'''

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera:
    def __init__(self):
        # taking the input from webcam
        #vid = cv2.VideoCapture(0)
        # from pi
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(camera, size=(640,480))
        pass

    def get_judgement(self):
        # running while loop just to make sure that
        # our program keep running untill we stop it
        #while True:
        #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True):
        # capturing the current frame
        #_, frame = vid.read()

        # displaying the current frame
        cv2.imshow("frame", self.rawCapture)

        # setting values for base colors
        b = self.rawCapture[:, :, :1]
        g = self.rawCapture[:, :, 1:2]
        r = self.rawCapture[:, :, 2:]

        # computing the mean
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)

        # displaying the most prominent color
        if (r_mean > g_mean and r_mean > b_mean):
            return "Red"
        else:
            return "White"
        #result = input("Type White or Red: >")
        #return result

def get_outcome():
    camera = Camera()
    judge = []
    good = 0
    no_good = 0
    for i in range(3):
        input("Press any key for next judgement")
        judge.append(camera.get_judgement())
        if judge[i] == "Red":
            no_good += 1
        elif judge[i] == "White":
            good += 1
    if good > no_good:
        outcome = "Pass"
    elif no_good > good:
        outcome = "Fail"

    return judge, outcome

if __name__ == "__main__":
    judge, outcome = get_outcome()
    print("Judge 1: " + judge[0])
    print("Judge 2: " + judge[1])
    print("Judge 3: " + judge[2])
    print("Outcome: " + outcome)
