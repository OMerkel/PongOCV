#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get a list of Video Capture IDs representing the available camera devices

Third Party Dependencies:
    Computer Vision Library OpenCV, https://opencv.org/

Copyright (c) 2021, Oliver Merkel.
Please see the AUTHORS file for details.
All rights reserved.

Use of this code is governed by a
MIT license that can be found in the LICENSE file.

"""

import cv2

def getVidCapIDs():
    result = []
    for i in range(100):
        try:
            print("Probe ID", i)
            cap = cv2.VideoCapture(i)
            if cap is not None and cap.isOpened():
                result.append(i)
        except:
            pass
    return result

if '__main__' == __name__:
    print(str(getVidCapIDs()))
