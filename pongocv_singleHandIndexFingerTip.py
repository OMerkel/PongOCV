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

import cv2
import mediapipe as mp
import time

major, minor, patchlevel = cv2.__version__.split(".")
assert major == "4", "Could not import OpenCV version 4"

class PongOCV:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.score = { "font": cv2.FONT_HERSHEY_SIMPLEX,
            "bottomLeft": (10, 40),
            "fontScale": 1,
            "fontColor": (255,255,255),
            "lineType": 2,
            "value": 0 }
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils

        ret, frame = self.cam.read()
        self.frameSizeY, self.frameSizeX, frameChannels = frame.shape

        self.frameSizeY, self.frameSizeX = (768, 1024)

        self.ball = { "x": 5, "y": 5,
            "dx": int(self.frameSizeX / 100), "dy": int(self.frameSizeX / 100),
            "radius": int(self.frameSizeX / 100) }
        self.paddle = { "x": 40, "y": self.frameSizeY-10, "dx": 5, "dy": 5,
            "sizex": int(self.frameSizeX / 10), "decay": 20 }

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def updateObjects(self):
        self.ball["x"] = self.ball["x"] + self.ball["dx"]
        self.ball["y"] = self.ball["y"] + self.ball["dy"]
        if self.ball["x"] < 0 or self.ball["x"] > self.frameSizeX:
            self.ball["dx"] = -self.ball["dx"]
        if self.ball["y"] < 0:
            self.ball["dy"] = -self.ball["dy"]
        if self.ball["y"] > self.frameSizeY:
            self.ball["dy"] = -self.ball["dy"]
        if self.ball["y"] >= self.paddle["y"]:
            self.ball["dy"] = -self.ball["dy"]
            if self.paddle["x"] < self.ball["x"] and \
                self.ball["x"] < self.paddle["x"] + self.paddle["sizex"]:
                self.score["value"] = self.score["value"] + 10

    def drawObjects(self, frame):
        # draw ball
        cv2.circle(frame, ( self.ball["x"], self.ball["y"] ), self.ball["radius"], (255, 255, 255), thickness=3)

        # draw paddle
        cv2.rectangle(frame, (int(self.paddle["x"]), self.paddle["y"]),
             (int(self.paddle["x"]+self.paddle["sizex"]), self.paddle["y"]+5), (255, 255, 255), thickness=3)

        cv2.putText(frame, str(self.score["value"]),
            self.score["bottomLeft"],
            self.score["font"],
            self.score["fontScale"],
            self.score["fontColor"],
            self.score["lineType"])
        cv2.imshow("Frame", frame)

    def run(self):
        pTime = 0
        cTime = 0
        key = 0
        while key!=27 and self.cam.isOpened():
            success, frame = self.cam.read()
            if not success:
                continue
            # horizontal mirror (notebook webcam and display used like a mirror)
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (self.frameSizeX, self.frameSizeY))
            h, w,_ = frame.shape
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frameRGB)
            if results.multi_hand_landmarks:
                for handLandmarks in results.multi_hand_landmarks:
                    indexTip = self.mpDraw._normalized_to_pixel_coordinates(
                        handLandmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].x,
                        handLandmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].y,
                        w, h)
                if indexTip is not None:
                    cx, cy = indexTip
                    cv2.circle(frame, (cx,cy), 10, (255,255,40), cv2.FILLED)
                    if cx > self.frameSizeX-self.paddle["sizex"]:
                        paddle_target_x = self.frameSizeX-self.paddle["sizex"]
                    else:
                        paddle_target_x = cx
                    self.paddle["x"] = int(
                        (self.paddle["decay"] * self.paddle["x"] + paddle_target_x) /
                        (self.paddle["decay"] + 1))

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(frame,str(int(fps)), (10,80), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3)
            self.updateObjects()
            self.drawObjects( frame )
            key = cv2.waitKey(1) & 0xff
        self.release()

if '__main__' == __name__:
    instance = PongOCV()
    instance.run()
