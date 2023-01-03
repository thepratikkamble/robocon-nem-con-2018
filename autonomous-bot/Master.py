import cv2
import numpy as np
import Camera
import time
from nanpy import (ArduinoApi, SerialManager)
import os

os.system("v4l2-ctl -d 1 -c white_balance_automatic=0")
os.system("v4l2-ctl -d 1 -c auto_exposure=1")
os.system("v4l2-ctl -d 1 -c gain_automatic=0")
os.system("v4l2-ctl -d 1 -c exposure=50")
os.system("v4l2-ctl -d 1 -c saturation=20")

connection = SerialManager()
a = ArduinoApi(connection=connection)



cap = cv2.VideoCapture(1)
a.analogWrite(20, 45)

framecount = 0
prevMillis = 0


cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


def fpsCount():
    global prevMillis
    global framecount
    millis = int(round(time.time() * 1000))
    framecount += 1
    if millis - prevMillis > 1000:
        print(framecount)
        prevMillis = millis
        framecount = 0

while True:

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([42,100,255], dtype=np.uint8)  #40, 90 blue  #43, 61 red

    mask = cv2.inRange(hsv, lower_white, upper_white)

    res = cv2.bitwise_and(frame,frame, mask= mask)

    kernel = np.ones((13,13),np.uint8)
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    gray= cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)


    fpsCount()

    cv2.imshow('res',thresh1)


    up = int(Camera.scan_up(thresh1))
    down = int(Camera.scan_down(thresh1))
    right = int(Camera.scan_right(thresh1))
    left = int(Camera.scan_left(thresh1))
    #print (up, down, right, left)
    a.analogWrite(21, up)
    a.analogWrite(22, down)
    a.analogWrite(23, right)
    a.analogWrite(24, left)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
