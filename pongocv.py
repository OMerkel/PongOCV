#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PongOCV

PongOCV is a solo Pong or Breakout alike game using Computer Vision via
live Webcam (e.g. camera from your notebook) to control your paddle.

Third Party Dependencies:
    Computer Vision Library OpenCV, https://opencv.org/

Copyright (c) 2021, Oliver Merkel.
Please see the AUTHORS file for details.
All rights reserved.

Use of this code is governed by a
MIT license that can be found in the LICENSE file.
"""

import cv2 as cv

major, minor, patchlevel = cv.__version__.split(".")
assert major == "4", "Could not import OpenCV version 4"

cam = cv.VideoCapture(0)
ret, frame = cam.read()
frameSizeY, frameSizeX, frameChannels = frame.shape

ball = { "x": 5, "y": 5, "dx": 5, "dy": 5, "radius": 5 }
key = 0
while key!=27 and cam.isOpened():
    ret, frame = cam.read()
    cv.circle(frame, ( ball["x"], ball["y"] ), ball["radius"], (255, 255, 255), thickness=3)
    cv.imshow("frame", frame)
    key = cv.waitKey(1) & 0xff
    ball["x"] = ball["x"] + ball["dx"]
    ball["y"] = ball["y"] + ball["dy"]
    if ball["x"] < 0 or ball["x"] > frameSizeX:
        ball["dx"] = -ball["dx"]
    if ball["y"] < 0 or ball["y"] > frameSizeY:
        ball["dy"] = -ball["dy"]
cv.destroyAllWindows()
