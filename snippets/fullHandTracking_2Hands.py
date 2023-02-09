#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full Hand Tracking - Two Hands

This code snippet implements a full hand tracking for two hands.
It highlights the IndexFingerTip and ThumbTip of both hands.

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

class fullHandTracking:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils

        ret, frame = self.cam.read()
        self.frameSizeY, self.frameSizeX, frameChannels = frame.shape

        self.frameSizeY, self.frameSizeX = (768, 1024)

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

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
                    thumbTip = self.mpDraw._normalized_to_pixel_coordinates(
                        handLandmarks.landmark[self.mpHands.HandLandmark.THUMB_TIP].x,
                        handLandmarks.landmark[self.mpHands.HandLandmark.THUMB_TIP].y,
                        w, h)
                    if thumbTip is not None:
                        cx, cy = thumbTip
                        cv2.circle(frame, (cx,cy), 10, (255,255,40), cv2.FILLED)
                    self.mpDraw.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(frame,str(int(fps)), (10,80), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xff
        self.release()

if '__main__' == __name__:
    instance = fullHandTracking()
    instance.run()
