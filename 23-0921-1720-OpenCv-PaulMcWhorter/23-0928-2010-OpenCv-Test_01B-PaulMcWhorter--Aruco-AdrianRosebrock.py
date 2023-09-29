# jwc 23-0928-2100 switch to RpCamV2: dtoverlay=imx219
# jwc 23-0928-2350 switch to RpCamV3-WideAngle: dtoverlay=imx708


import cv2
from picamera2 import Picamera2
import time

# Aruco Markers
import imutils
import argparse
import sys


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
    default="DICT_ARUCO_ORIGINAL",
    help="type of ArUCo tag to detect")

args = vars(ap.parse_args())


# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

###jwc n ARUCO_DICT = {
###jwc n     "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
###jwc n }


piCam = Picamera2()
# for 30fps
###jwc o piCam.preview_configuration.size=(1280,720)
###jwc o 2fps: piCam.preview_configuration.main.size=(1280,720)
###jwc y 6-7fps: piCam.preview_configuration.main.size=(640,360)

# jwc y 26-27fps
###jwc yyy piCam.preview_configuration.main.size=(320,180)
###jwc ? slower: piCam.preview_configuration.main.size=(620,360)

###jwc yyy 90fps, im:225150 : piCam.preview_configuration.main.size=(320,180)
###jwc yy little more glitchier/laggier: piCam.preview_configuration.main.size=(640,360)
# jwc seems fine as dimensions grow
piCam.preview_configuration.main.size=(1280,720)

###jwc o piCam.preview_configuration.__format__="RGB888"
piCam.preview_configuration.main.format="RGB888"
#jwc seems to work noton UsbCam  C720 nor C922 but on CsiCam:Lanzo RpiClone
###jwc y but only 1-2 fps: piCam.preview_configuration.controls.FrameRate=30
###jwc y 22-24fps, try 90: piCam.preview_configuration.controls.FrameRate=60
# jwc 23-0927-1200 TYJ fps rose to 25-28fps :)+, even with GUI, VsCode, SSH: 95tasks, 122threads :)+
###jwc 23-0928-1330 yy piCam.preview_configuration.controls.FrameRate=90
###jwc from 12 to 48fps: piCam.preview_configuration.controls.FrameRate=100
###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=120
###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=100
###jwc y piCam.preview_configuration.controls.FrameRate=99

###jwc 23-0929-1050 20-30fps: piCam.preview_configuration.controls.FrameRate=60
piCam.preview_configuration.controls.FrameRate=90
piCam.preview_configuration.align()


framecount = 0
prevMillis = 0
def fpsCount():
    global prevMillis
    global framecount
    millis = int(round(time.time() * 1000))
    framecount += 1
    if millis - prevMillis > 1000:
        print(framecount)
        prevMillis = millis 
        framecount = 0
        

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
        args["type"]))
    sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
###jwc o,n arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
###jwc o,n arucoParams = cv2.aruco.DetectorParameters_create()

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
arucoParams =  cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)


piCam.configure("preview")
piCam.start()

# jwc Provide time to stabilize
time.sleep(2.0)

while True:
    frame = piCam.capture_array()
    

    ###jwc y 2-3fps CsiCam Lanzo seems good (better vs. CsiPiCam2): frame = imutils.resize(frame, width=1000)
    ###jwc y 7-8 fps: frame = imutils.resize(frame, width=500)
    ###jwc y 17-18fps frame = imutils.resize(frame, width=250)
    ###jwc y 33-35fps frame = imutils.resize(frame, width=125)
    ###jwc yy 15-16fps seems just right
    ###jwc yy same fps for CsiCam_Lanzo_PiCamClone
    ###jwc yy frame = imutils.resize(frame, width=320)
    ###jwc yyy 19-20fps with 'height' added and now h,w in sync w/ above 'VideoStream' :)+
    #jwc 'VideoStream: h,w' should be in sync w/ 'imutils.resize: h,w' :)+
    ###jwc y: frame = imutils.resize(frame, height=320, width=240)
    ###jwc y frame = imutils.resize(frame, height=160, width=120)
    ###jwc videostream 80,60  30fps seems but shows 6-8fps
    ###jwc frame = imutils.resize(frame, height=1600, width=1200)
    ###jwc yy frame = imutils.resize(frame, height=800, width=600)
    ###jwc y frame = imutils.resize(frame, height=1200, width=900)
    ###jwc y frame = imutils.resize(frame, height=1000, width=750)
    ###jwc y frame = imutils.resize(frame, height=800, width=600)
    ###jwc yy frame = imutils.resize(frame, height=400, width=300)
    ###jwc 1-2 sec lag: frame = imutils.resize(frame, height=750, width=500)
    
    ###jwc 23-0928-2300 wow 8-10 fps: frame = imutils.resize(frame, height=600, width=400)
    ###jwc y 15-25fps: frame = imutils.resize(frame, height=300, width=200)
    ###jwc y 20-25fps: frame = imutils.resize(frame, height=450, width=300)
    
    # jwc imx219
    #
    ###jwc yy jumped from 20-25fps to 48fps >> since > 30fps very real-time but small screen :)+
    ###jwc y 35fps: frame = imutils.resize(frame, height=225, width=150)

    # jwc imx708 non-wide
    #
    ###jwc y now w/ imx708 non_wide: 35fps: frame = imutils.resize(frame, height=225, width=150)
    ###jwc y 28fps: frame = imutils.resize(frame, height=450, width=300)
    ###jwc y 29 fps: frame = imutils.reszie(frame, height=400, width=300)
    ###jwc y 25 fps: frame = imutils.resize(frame, height=375, width=300)
    ###jwc y 33fps :)+
    frame = imutils.resize(frame, height=350, width=250)
    
    # detect ArUco markers in the input frame
    ###jwc o (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    (corners, ids, rejected) = arucoDetector.detectMarkers(frame)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned
            # in top-left, top-right, bottom-right, and bottom-left
            # order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
   
            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

            # compute and draw the center (x, y)-coordinates of the
            # ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

            # draw the ArUco marker ID on the frame
            cv2.putText(frame, str(markerID),
                (topLeft[0], topLeft[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    
    
    cv2.imshow("piCam", frame)
            
    fpsCount()
    
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()
