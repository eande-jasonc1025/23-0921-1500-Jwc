# jwc 23-1011-1800 When you now run the program, you will notice that the heading stays the same value if the magnetometer is tilted to within 40 degrees.

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

import math


# jwc Low Pass Filter
#
MAG_LPF_FACTOR = 0.4
ACC_LPF_FACTOR = 0.1


def runExample():
    
    oldXMagRawValue = 0
    oldYMagRawValue = 0
    oldZMagRawValue = 0
    oldXAccRawValue = 0
    oldYAccRawValue = 0
    oldZAccRawValue = 0
    
    # jwc 'sys.argv[2] is 'mode_Int'
    #
    if len(sys.argv) >= 2:
        mode_Int = int(sys.argv[1])
    else:
        mode_Int = 0
    print("*** Mode [0|1]: ", mode_Int)


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

            # Apply low pass filter to reduce noise
            #
            IMU.mxRaw =  IMU.mxRaw  * MAG_LPF_FACTOR + oldXMagRawValue*(1 - MAG_LPF_FACTOR);
            IMU.myRaw =  IMU.myRaw  * MAG_LPF_FACTOR + oldYMagRawValue*(1 - MAG_LPF_FACTOR);
            IMU.mzRaw =  IMU.mzRaw  * MAG_LPF_FACTOR + oldZMagRawValue*(1 - MAG_LPF_FACTOR);
            IMU.axRaw =  IMU.axRaw  * ACC_LPF_FACTOR + oldXAccRawValue*(1 - ACC_LPF_FACTOR);
            IMU.ayRaw =  IMU.ayRaw  * ACC_LPF_FACTOR + oldYAccRawValue*(1 - ACC_LPF_FACTOR);
            IMU.azRaw =  IMU.azRaw  * ACC_LPF_FACTOR + oldZAccRawValue*(1 - ACC_LPF_FACTOR);
            #
            oldXMagRawValue = IMU.mxRaw
            oldYMagRawValue = IMU.myRaw
            oldZMagRawValue = IMU.mzRaw
            oldXAccRawValue = IMU.axRaw
            oldYAccRawValue = IMU.ayRaw
            oldZAccRawValue = IMU.azRaw

            # jwc Since Rotational Direction is reversed, must inverse the polarity so that clockwise, angle ^.
            # jwc DOESN'T MATTER WHICH IS NEGATIVE-INVERTED, BUT JUST ONE NOT BOTH
            ###jwc n IMU.mxRaw *= -1
            IMU.mxRaw *= -1
            ###jwc y IMU.myRaw *= -1
             
            botHeadingNow_Degrees = 180 * (math.atan2(IMU.myRaw, IMU.mxRaw)/math.pi)
            if botHeadingNow_Degrees < 0:
                    botHeadingNow_Degrees+=360
                    

            ###jwc o accXnorm = accRaw[0]/sqrt(accRaw[0]* accRaw[0]+ accRaw[1] * accRaw[1] + accRaw[2] * accRaw[2]);
            ###jwc o accYnorm = accRaw[1]/sqrt(accRaw[0] *accRaw[0] + accRaw[1] * accRaw[1] + accRaw[2] * accRaw[2]);                    
            accXnorm = IMU.axRaw/math.sqrt(IMU.axRaw * IMU.axRaw + IMU.ayRaw * IMU.ayRaw + IMU.azRaw * IMU.azRaw)
            accYnorm = IMU.ayRaw/math.sqrt(IMU.axRaw * IMU.axRaw + IMU.ayRaw * IMU.ayRaw + IMU.azRaw * IMU.azRaw)
            
            ###jwc o pitch = asin(accXnorm);
            ###jwc o roll = -asin(accYnorm/cos(pitch));         
            pitch = math.asin(accXnorm)
            roll = -math.asin(accYnorm/math.cos(pitch))

            # jwc //Calculate the new tilt compensated values
            # jwc //The compass and accelerometer are orientated differently on the the BerryIMUv1, v2 and v3.
            # jwc //needs to be taken into consideration when performing the calculations
            # jwc //X compensation
            ###jwc o if(BerryIMUversion == 1 || BerryIMUversion == 3)
            ###jwc o 	magXcomp = magRaw[0]*cos(pitch)+magRaw[2]*sin(pitch);
            ###jwc o else if (BerryIMUversion == 2)
            ###jwc o 	magXcomp = magRaw[0]*cos(pitch)-magRaw[2]*sin(pitch);
            ###jwc o 
            ###jwc o //Y compensation
            ###jwc o if(BerryIMUversion == 1 || BerryIMUversion == 3)
            ###jwc o 	magYcomp = magRaw[0]*sin(roll)*sin(pitch)+magRaw[1]*cos(roll)-magRaw[2]*sin(roll)*cos(pitch); // LSM9DS0
            ###jwc o else if (BerryIMUversion == 2)
            ###jwc o 	magYcomp = magRaw[0]*sin(roll)*sin(pitch)+magRaw[1]*cos(roll)+magRaw[2]*sin(roll)*cos(pitch); // LSM9DS1
            
            if mode_Int == 0:
                # Plan A
                #
                # jwc X compensation
                magXcomp = IMU.mxRaw*math.cos(pitch)+IMU.mzRaw*math.sin(pitch)
                # jwc Y compensation
                magYcomp = IMU.mxRaw*math.sin(roll)*math.sin(pitch)+IMU.myRaw*math.cos(roll)-IMU.mzRaw*math.sin(roll)*math.cos(pitch)
            else:
                # Plan B
                #
                # jwc X compensation
                ###jwc ? magXcomp = IMU.mxRaw*math.cos(pitch)-IMU.mzRaw*math.sin(pitch)
                magXcomp = IMU.mxRaw*math.cos(pitch)+IMU.mzRaw*math.sin(pitch)
                # jwc Y compensation
                magYcomp = IMU.mxRaw*math.sin(roll)*math.sin(pitch)+IMU.myRaw*math.cos(roll)+IMU.mzRaw*math.sin(roll)*math.cos(pitch)


            botHeadingNow_TiltCompensated_Degrees = 180 * (math.atan2(magYcomp, magXcomp)/math.pi)
            if botHeadingNow_TiltCompensated_Degrees < 0:
                    botHeadingNow_TiltCompensated_Degrees += 360            

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
                    'Node: {:01d}'.format(mode_Int)\
            ##jwc y , '\t', 'aX: {:06d}'.format(IMU.axRaw)\
            ##jwc y , '\t', 'aY: {:06d}'.format(IMU.ayRaw)\
            ##jwc y , '\t', 'aZ: {:06d}'.format(IMU.azRaw)\
            ##jwc y , '\t', 'gX: {:06d}'.format(IMU.gxRaw)\
            ##jwc y , '\t', 'gY: {:06d}'.format(IMU.gyRaw)\
            ##jwc y , '\t', 'gZ: {:06d}'.format(IMU.gzRaw)\
            ##jwc y , '\t', 'mX: {:06d}'.format(IMU.mxRaw)\
            ##jwc y , '\t', 'mY: {:06d}'.format(IMU.myRaw)\
            ##jwc y , '\t', 'mZ: {:06d}'.format(IMU.mzRaw)\
            , '\t', 'Hd: {:.2f}'.format(botHeadingNow_Degrees)\
            , '\t', 'Hd: {:.2f}'.format(botHeadingNow_TiltCompensated_Degrees)\
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


