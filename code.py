#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:02:28 2021

@author: vishnutammishetti
"""

import cv2 as cv
import numpy as np
from collections import deque

def dump(x):
   pass





idx = 0


paint = np.zeros((471,636,3)) + 255

cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)

videoFeed = cv.VideoCapture(0)




def filterFrame(colorSpace, lower, upper):
    return cv.inRange(colorSpace, lower, upper)

def performErosion(filter, kernel, iterations = 1):
    return cv.erode(filter, kernel, iterations)

def getDilatedFrame(erodedFrame):
    temp = cv.morphologyEx(erodedFrame, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return cv.dilate(erodedFrame, np.ones((5,5),np.uint8), iterations=1)
    
def getHSV(frame):
    rame = cv.flip(frame, 1)
    return cv.cvtColor(frame, cv.COLOR_BGR2HSV)

def getCenter(contours):
    contours = sorted(contours, key = cv.contourArea, reverse = True)[0]
        
    coords, radius = cv.minEnclosingCircle(contours)
    x, y = coords[0], coords[1]
    cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        
    M = cv.moments(contours)
    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
    
    return center

def drawLine(lines, frame, paint, colors):
    for idx in range(len(lines)):
        for jdx in range(len(lines[idx])):
            for mdx in range(1, len(lines[idx][jdx])):
                if lines[idx][jdx][mdx - 1] is None or lines[idx][jdx][mdx] is None:
                    continue
                cv.line(frame, lines[idx][jdx][mdx - 1], lines[idx][jdx][mdx], colors[idx], 2)
                cv.line(paint, lines[idx][jdx][mdx - 1], lines[idx][jdx][mdx], colors[idx], 2)
                
    return frame, paint



def putFrame(frame):
    colorHSVs = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    frame = cv.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv.rectangle(frame, (160,1), (255,65), colorHSVs[3], -1)
    frame = cv.rectangle(frame, (275,1), (370,65), colorHSVs[2], -1)
    frame = cv.rectangle(frame, (390,1), (485,65), colorHSVs[1], -1)
    frame = cv.rectangle(frame, (505,1), (600,65), colorHSVs[0], -1)
    cv.putText(frame, "Erase", (49, 33), cv.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    
    
    cv.putText(frame, "", (420, 33), cv.FONT_ITALIC, 0.5, (150,150,150), 2, cv.LINE_AA)
    cv.putText(frame, "", (298, 33), cv.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "", (185, 33), cv.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "", (520,33), cv.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    
    return frame

def getContours(maskedFrame):
    contours, hierarchy = cv.findContours(maskedFrame.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    return contours

while True:
    returnVal, frame = videoFeed.read()
    colorHSVs = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    
    hsv = getHSV(frame)
    
    upperHSV = np.array([153, 255, 255])
    lowerHSV = np.array([64, 72, 48])
    
    frame = putFrame(frame)
    filter = filterFrame(hsv, lowerHSV, upperHSV)
    erodedFrame = performErosion(filter, np.ones((5,5),np.uint8), 1)
    maskedFrame = getDilatedFrame(erodedFrame)
    contours = getContours(maskedFrame)
    
    center = None

    
    if len(contours):
        
        center = getCenter(contours)
        xCenter = center[0]
        yCenter = center[1]

        
        if yCenter <= 65:
            if 40 <= xCenter <= 140: 
                blueLines, idxBlue = [deque()], 0
                greenLines, idxGreen = [deque()], 0
                redLines, idxRed = [deque()], 0
                yellowLines, idxYellow = [deque()], 0


                paint[67:,:,:] = 255
            else:
                if 160 <= xCenter and xCenter <= 255:
                    idx = 3 
                else:
                    if 275 <= xCenter and xCenter  <= 370:
                        idx = 2 
                    else:
                        if 390 <= xCenter and xCenter <= 485:
                            idx = 1 
                        else:
                            if 505 <= xCenter and xCenter  <= 600:
                                idx = 0 
        else :
            if idx == 0:
                blueLines[idxBlue].appendleft(center)
            else:
                if idx == 1:
                    greenLines[idxGreen].appendleft(center)
                else:
                    if idx == 2:
                        redLines[idxRed].appendleft(center)
                    else:
                        if idx == 3:
                            yellowLines[idxYellow].appendleft(center)
    else:
        
        idxBlue += 1
        idxYellow += 1
        idxGreen += 1
        idxRed += 1
        yellowLines.append(deque())
        blueLines.append(deque())
        greenLines.append(deque())
        redLines.append(deque())
        

    lines = [blueLines, greenLines, redLines, yellowLines]
    
    frame, paintWindow = drawLine(lines, frame, paint, colorHSVs)


    cv.imshow("Transparent frame", frame)
    cv.imshow("Sketch pad", paintWindow)
    cv.imshow("mask",maskedFrame)


    if cv.waitKey(1) & 0xFF == ord("q"):
        break

        

