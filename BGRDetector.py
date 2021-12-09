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
        self.rawCapture = PiRGBArray(self.camera, size=(640,480))
    
    def deinit(self):
        self.camera.close()

    def get_judgement(self):
        # running while loop just to make sure that
        # our program keep running untill we stop it
        #while True:
        #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        # capturing the current frame
        #_, frame = vid.read()
        img = self.rawCapture.array


        # setting values for base colors
        b = img[:, :, 0]
        g = img[:, :, 1]
        r = img[:, :, 2]

        # computing the mean
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)
        
        print("Means: blue-" + str(b_mean) + " green-" + str(g_mean) + " red-" + str(r_mean))
        
        self.rawCapture.truncate(0)
        # displaying the most prominent color
        if (r_mean > g_mean and r_mean > b_mean):
            return False
        else:
            return True
        #result = input("Type White or Red: >")
        #return result

def get_outcome():
    camera = Camera()
    judge = []
    outcome = False
    good = 0
    no_good = 0
    for i in range(3):
        input("Press the enter key for judge: " + str(i + 1))
        judge.append(camera.get_judgement())
        if judge[i] == True:
            good += 1
        else:
            no_good += 1
    if good > 1:
        outcome = True
    camera.deinit()
    return judge, outcome

if __name__ == "__main__":
    judge, outcome = get_outcome()
    print("Judge 1: " + str(judge[0]))
    print("Judge 2: " + str(judge[1]))
    print("Judge 3: " + str(judge[2]))
