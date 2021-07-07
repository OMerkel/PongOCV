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

major, minor, patchlevel = cv2.__version__.split(".")
assert major == "4", "Could not import OpenCV version 4"

def callback(x):
    pass

class PongOCV:

    def initUi(self):
        self.cam = cv2.VideoCapture(0)
        self.score = { "font": cv2.FONT_HERSHEY_SIMPLEX,
            "bottomLeft": (10, 40),
            "fontScale": 1,
            "fontColor": (255,255,255),
            "lineType": 2,
            "value": 0 }
        cv2.namedWindow( "Control", cv2.WINDOW_AUTOSIZE )
        cv2.createTrackbar( "lowerHue", "Control", 1, 255, callback)
        cv2.createTrackbar( "upperHue", "Control", 1, 255, callback)
        cv2.createTrackbar( "lowerSat", "Control", 1, 255, callback)
        cv2.createTrackbar( "upperSat", "Control", 1, 255, callback)
        cv2.createTrackbar( "lowerVal", "Control", 1, 255, callback)
        cv2.createTrackbar( "upperVal", "Control", 1, 255, callback)
        """
        blue default paddle control color
        """
        cv2.setTrackbarPos( "lowerHue", "Control", 35 )
        cv2.setTrackbarPos( "upperHue", "Control", 105 )
        cv2.setTrackbarPos( "lowerSat", "Control", 5 )
        cv2.setTrackbarPos( "upperSat", "Control", 100 )
        cv2.setTrackbarPos( "lowerVal", "Control", 45 )
        cv2.setTrackbarPos( "upperVal", "Control", 77 )

    def initCamera(self):
        ret, frame = self.cam.read()
        self.frameSizeY, self.frameSizeX, frameChannels = frame.shape

    def initObjects(self):
        self.ball = { "x": 5, "y": 5, "dx": 5, "dy": 5, "radius": 5 }
        self.paddle = { "x": 40, "y": self.frameSizeY-10, "dx": 5, "dy": 5,
            "sizex": 60, "decay": 20 }

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
            if self.paddle["x"] - self.paddle["sizex"] / 2 < self.ball["x"] and \
                self.ball["x"] < self.paddle["x"] + self.paddle["sizex"] / 2:
                self.score["value"] = self.score["value"] + 10

    def drawObjects(self, frame):
        # draw ball
        cv2.circle(frame, ( self.ball["x"], self.ball["y"] ), self.ball["radius"], (255, 255, 255), thickness=3)

        # draw paddle
        cv2.rectangle(frame, (int(self.paddle["x"]-self.paddle["sizex"]/2), self.paddle["y"]),
             (int(self.paddle["x"]+self.paddle["sizex"]/2), self.paddle["y"]+5), (255, 255, 255), thickness=3)

        # horizontal mirror (notebook webcam and display used like a mirror)
        frame2 = frame.copy()
        frame2 = cv2.flip(frame, 1)

        cv2.putText(frame2, str(self.score["value"]),
            self.score["bottomLeft"],
            self.score["font"],
            self.score["fontScale"],
            self.score["fontColor"],
            self.score["lineType"])

        # show frame
        cv2.imshow("frame", frame2)

    def run(self):
        self.initUi()
        self.initCamera()
        self.initObjects()
        key = 0
        while key!=27 and self.cam.isOpened():
            ret, frame = self.cam.read()
    
            # convert to HSV to ease filtering for color range
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            self.targetColor = {
                "lower" : (cv2.getTrackbarPos("lowerHue", "Control"),
                           cv2.getTrackbarPos("lowerSat", "Control"),
                           cv2.getTrackbarPos("lowerVal", "Control")),
                "upper" : (cv2.getTrackbarPos("upperHue", "Control"),
                           cv2.getTrackbarPos("upperSat", "Control"),
                           cv2.getTrackbarPos("upperVal", "Control")) }
            mask = cv2.inRange(frame,
                               self.targetColor['lower'],
                               self.targetColor['upper'])

            # get contours in mask holding target color parts
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # determine biggest contour in terms of contour area size
            if len(contours) > 0:
                controlObject = max(contours, key=cv2.contourArea)

                # draw bounding box
                x, y, w, h = cv2.boundingRect(controlObject)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), thickness=3)

                self.paddle["x"] = int((self.paddle["decay"] *
                    self.paddle["x"] + x + w / 2) / (self.paddle["decay"] + 1))
            self.updateObjects()
            self.drawObjects( frame )
    
            key = cv2.waitKey(1) & 0xff
        self.release()

if '__main__' == __name__:
    instance = PongOCV()
    instance.run()
