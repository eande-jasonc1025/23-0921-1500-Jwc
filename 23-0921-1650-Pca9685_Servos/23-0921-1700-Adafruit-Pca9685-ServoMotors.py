from adafruit_servokit import ServoKit
from time import sleep

servoKit_Pca9685_Pin_MotorLeft = 0
servoKit_Pca9685_Pin_MotorRight = 1

servoKit_Object = ServoKit(channels=16)

###jwc y servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=90
###jwc y print("90")
###jwc y sleep(3.0)
###jwc y servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
###jwc y print("120")
###jwc y sleep(3.0)
###jwc y servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=150
###jwc y print("150")
###jwc y sleep(3.0)

while True:

   print("Set value range -1.0 to +1.0")
   for value in range(180,-10,-10):
      servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=value
      servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=value
      print(value)
      sleep(3.0)
