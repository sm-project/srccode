

#path setting
import sys
#sys.path.insert(0, "/home/pi/exam/RpiSetup/remote_control/remote_control")
from driver import camera, stream, wheels,esc_1060
import light
import pickle
import threading
import ino
import time

#initialization
db_file = "/home/pi/remote_control/remote_control/driver/config"
f = open('/home/pi/remote_control/remote_control/calibration_data')
drive_n = pickle.load(f)
ardu = ino.Ino()
steer_n = pickle.load(f)
print 'drive_n = ', drive_n, 'steer_n = ', steer_n
esc = esc_1060.ESC(1, 0x40,60, 10, 11,drive_n,steer_n)
EMERGENCY_FLAG = False
##################################################################3######

def timer_sonic():
	time.sleep(0.5)
	count_flag = 0
	EMERGENCY_FLAG = False
	
	dist = 1000
	
	while True:
		dist = ardu.sonic()
		try: 
			dist = float(dist)
#			print "dist = ", dist
		except:
			pass
		
		if count_flag < 30 and dist < 10:
			count_flag += 1

		if count_flag >= 30 :
			EMERGENCY_FLAG = True
			print "EMERGENCY"
			time.sleep(0.5)
			esc.stop()
#			count_flag -= 1
		if dist > 100 and EMERGENCY_FLAG:
			count_flag -= 1
			


th1 = threading.Thread(target=timer_sonic)
th1.start()


'''
li = light.Light()
t1 = threading.Thread(target = li.left())
'''
SPEED = 100

key = 0
#########

#########
#input command
esc.set_speed(4)

while key != 'q':
	
	key = raw_input("give command : ")
	print "input key : [" + key + "]"
	
	dis = ardu.sonic()

	'''
	try:	
		dis1 = float(dis)
		print dis1
		if dis1 < float(30.0):
			print "EMERGENCY"
			EMEMERGENCY_FLAG = 0
	except:
		pass
	'''

	if EMERGENCY_FLAG > 100:
			EMERGENCY_FLAG = 0

	#move forward
	if key == "w":
		print "[forward]\n"
	
		#TODO
		esc.forward()

	#move backward
	elif key == 's':
		print "[backward]\n"

		#TODO
		esc.backward()



	#turn left
	elif key == 'a':
		print "[turn left]\n"
		esc.left()
		#TODO
#		li.left()
#		t1.start()


	#turn right
	elif key == 'd':
		print "[turn right]\n"
		esc.stop()
		#TODO
#		li.right()


	#exit
	elif key == 'q':
		print "[stop] entered\n"
		
	#TO		
		sys.exit()

	#wrong input
	else :
		print "Wrong Input Command\n"
