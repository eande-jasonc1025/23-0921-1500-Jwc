import cv2
from picamera2 import Picamera2
import time

piCam = Picamera2()
# for 30fps
###jwc o piCam.preview_configuration.size=(1280,720)
###jwc o 2fps: piCam.preview_configuration.main.size=(1280,720)
###jwc y 6-7fps: piCam.preview_configuration.main.size=(640,360)
# jwc y 26-27fps
piCam.preview_configuration.main.size=(320,180)
###jwc o piCam.preview_configuration.__format__="RGB888"
piCam.preview_configuration.main.format="RGB888"
#jwc seems to work noton UsbCam  C720 nor C922 but on CsiCam:Lanzo RpiClone
###jwc y but only 1-2 fps: piCam.preview_configuration.controls.FrameRate=30
###jwc y 22-24fps, try 90: piCam.preview_configuration.controls.FrameRate=60
# jwc 23-0927-1200 TYJ fps rose to 25-28fps :)+, even with GUI, VsCode, SSH: 95tasks, 122threads :)+
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

piCam.configure("preview")
piCam.start()

while True:
    frame = piCam.capture_array()
    cv2.imshow("piCam", frame)
    
    fpsCount()
    
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()
