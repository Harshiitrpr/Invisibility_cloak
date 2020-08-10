# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 17:22:33 2020

@author: Harshwardhan
"""

import cv2
#from cv2 import bitwise_and as And
from cv2 import bitwise_not as Not
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Tuning")
cv2.createTrackbar("LH", "Tuning", 67, 255, nothing)
cv2.createTrackbar("LS", "Tuning", 51, 255, nothing)
cv2.createTrackbar("LV", "Tuning", 116, 255, nothing)
cv2.createTrackbar("UH", "Tuning", 134, 255, nothing)
cv2.createTrackbar("US", "Tuning", 255, 255, nothing)
cv2.createTrackbar("UV", "Tuning", 255, 255, nothing)

switch = 8


result = True
while(result):
    switch = cv2.waitKey(1)
    ret,frame = cap.read()
    cv2.imshow("frame", frame) 
    if switch == 27:
        while(result):
            cv2.imwrite("background.jpg",frame)
            result = False

background = cv2.imread('background.jpg',-1)
while True:

     _, frame = cap.read()
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

     l_h = cv2.getTrackbarPos("LH", "Tuning")
     l_s = cv2.getTrackbarPos("LS", "Tuning")
     l_v = cv2.getTrackbarPos("LV", "Tuning")

     u_h = cv2.getTrackbarPos("UH", "Tuning")
     u_s = cv2.getTrackbarPos("US", "Tuning")
     u_v = cv2.getTrackbarPos("UV", "Tuning")
     
     l_b = np.array([l_h, l_s, l_v])
     u_b = np.array([u_h, u_s, u_v])
     
     kernel = np.ones((5, 5), np.uint8)

     mask = cv2.inRange(hsv, l_b, u_b)
     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
     mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
     mask_img = cv2.bitwise_and(background, background, mask = mask)


     res = cv2.bitwise_and(frame, frame, mask = Not(mask))
#     final_res = cv2.add(mask_img, res)
     cv2.imshow("frame", frame)
#     cv2.imshow("mask", mask)
     cv2.imshow("res", res)
#     cv2.imshow("mask_img", mask_img)
     cv2.imshow("final_res", mask_img + res)
     key = cv2.waitKey(1)
     if key == 27:
         break

cap.release()
cv2.destroyAllWindows()