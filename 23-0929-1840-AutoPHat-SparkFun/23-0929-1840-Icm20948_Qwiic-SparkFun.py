#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex1_qwiic_ICM20948.py
#
# Simple Example for the Qwiic ICM20948 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, March 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

from __future__ import print_function
import qwiic_icm20948
import time
import sys

def runExample():

    print("\nSparkFun 9DoF ICM-20948 Sensor  Example 1\n")
    IMU = qwiic_icm20948.QwiicIcm20948()

    if IMU.connected == False:
        print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    IMU.begin()

    while True:
        if IMU.dataReady():
            IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
            ###jwc y TYJ: print(\
            ###jwc y TYJ:         '{: 06d}'.format(IMU.axRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.ayRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.azRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.gxRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.gyRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.gzRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.mxRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.myRaw)\
            ###jwc y TYJ: , '\t', '{: 06d}'.format(IMU.mzRaw)\
            ###jwc y TYJ: )
            print(\
                    'aX: {: 06d}'.format(IMU.axRaw)\
            , '\t', 'aY: {: 06d}'.format(IMU.ayRaw)\
            , '\t', 'aZ: {: 06d}'.format(IMU.azRaw)\
            , '\t', 'gX: {: 06d}'.format(IMU.gxRaw)\
            , '\t', 'gY: {: 06d}'.format(IMU.gyRaw)\
            , '\t', 'gZ: {: 06d}'.format(IMU.gzRaw)\
            , '\t', 'mX: {: 06d}'.format(IMU.mxRaw)\
            , '\t', 'mY: {: 06d}'.format(IMU.myRaw)\
            , '\t', 'mZ: {: 06d}'.format(IMU.mzRaw)\
            )
            ###jwc o time.sleep(0.03)
            time.sleep(0.1)
        else:
            print("Waiting for data")
            time.sleep(0.5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
