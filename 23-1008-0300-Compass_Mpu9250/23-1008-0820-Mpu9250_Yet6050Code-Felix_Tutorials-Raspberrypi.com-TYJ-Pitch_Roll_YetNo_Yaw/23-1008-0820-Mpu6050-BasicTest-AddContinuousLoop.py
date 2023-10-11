# jwc https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/

#!/usr/bin/python
import smbus
import math
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
	###jwc o print ("Gyroskop")
	###jwc o print ("--------")
	###jwc o  
	###jwc o gyroskop_xout = read_word_2c(0x43)
	###jwc o gyroskop_yout = read_word_2c(0x45)
	###jwc o gyroskop_zout = read_word_2c(0x47)
	###jwc o  
	###jwc o print ("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
	###jwc o print ("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
	###jwc o print ("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
	###jwc o  
	###jwc o print
	###jwc o print ("Beschleunigungssensor")
	###jwc o print ("---------------------")
	###jwc o  
	###jwc o beschleunigung_xout = read_word_2c(0x3b)
	###jwc o beschleunigung_yout = read_word_2c(0x3d)
	###jwc o beschleunigung_zout = read_word_2c(0x3f)
	###jwc o  
	###jwc o beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
	###jwc o beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
	###jwc o beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
	###jwc o  
	###jwc o print ("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert)
	###jwc o print ("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert)
	###jwc o print ("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert)
	###jwc o  
	###jwc o print ("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
	###jwc o print ("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
	###jwc o 
	
	gyroskop_xout = read_word_2c(0x43)
	gyroskop_yout = read_word_2c(0x45)
	gyroskop_zout = read_word_2c(0x47)
	
	beschleunigung_xout = read_word_2c(0x3b)
	beschleunigung_yout = read_word_2c(0x3d)
	beschleunigung_zout = read_word_2c(0x3f)
	
	beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
	beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
	beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
	
	rotation_X_Deg = get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
	rotation_Y_Deg = get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
	
	###jwc ? print ("GYRO: %5d %6.2f, %5d %6.2f, %5d %6.2f" % (gyroskop_xout, (gyroskop_xout / 131), gyroskop_yout, (gyroskop_yout / 131))
	print ("*** %8.2f %8.2f %8.2f | %8.2f %8.2f %8.2f | %8.2f %8.2f" % ( gyroskop_xout, gyroskop_yout, gyroskop_zout, beschleunigung_xout, beschleunigung_yout, beschleunigung_zout, rotation_X_Deg, rotation_Y_Deg))
	


