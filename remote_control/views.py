'''
**********************************************************************
* Filename    : viewsws
* Description : views for server
* Author      : Sangyun.Kwon
* Brand       : MagicEco
* Website     : www.magice.co
* Update      : Sangyun.Kwon    2019-03-24    New release
**********************************************************************
'''

from django.shortcuts import render_to_response
#from driver import stream
from django.http import HttpResponse
import os
from remote_control.driver import camera, esc_1060,stream
import pickle
import light
import ts
import threading

li = light.Light()
import httplib, urllib
import time
import smbus
bus = smbus.SMBus(1)
global dat
dat = 0x48
key = 'NKP3ZABMT8W2YD8O'
global flag
flag = True

def thermometer():
	global flag
	while True:
		bus.write_byte(dat,0x70)
		temp = bus.read_byte(dat)
		bus.write_byte(dat,0x48)
		regi = bus.read_byte(dat)
 		params = urllib.urlencode({'field1': temp, 'field2': regi, 'key': key})
		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": 'text/plain'}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")
		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			print "Send"
			data = response.read()
			conn.close()
		except:
			print "Fail"
		if not flag:
			break
		time.sleep(8)


t1 = threading.Thread(target=thermometer)

def get_stored_value():
    try:
        file = open('/home/pi/remote_control/remote_control/calibration_data', 'r+b')
        drive_neutral = pickle.load(file)
        steer_center = pickle.load(file)
        file.close
    except:
        drive_neutral = 369
        steer_center = 390

    print "drive_n : ",drive_neutral
    print "steer_c : ",steer_center
    return drive_neutral, steer_center


db_file = "./driver/config"
drive_n, steer_c = get_stored_value()
esc = esc_1060.ESC(1, 0x40, 60, 10, 11, drive_n, steer_c)

cam = camera.Camera(debug=False, db=db_file, address = 0x40)
SPEED = 60

print stream.start()


def home(request):
    return render_to_response("base.html")

def run(request):

    global SPEED, bw_status, flag
    debug = ''
    """
    # ============== linetrack ==============
    if 'linetrack' in request.GET:
        with open('/home/pi/remote_control/remote_control/line_tracker.py',"r") as lnt:
            exec(lnt.read())
        #exec(open("/home/pi/remote_control/remote_control/line_tracker.py").read())
        #os.system('/home/pi/remote_control/remote_control/line_tracker.py')
    """
    if 'action' in request.GET:
        action = request.GET['action']
    # ============== Back wheels =============
        if action == 'bwready':

            esc.stop()
        elif action == 'sense':	   
	    if flag:
		flag = False
		print "End"
#		t1.start()
	    else:
		print "Start"
		flag = True
		if not t1.is_alive():
			t1.start()

	elif action == 'forward':

            esc.forward()
            debug = "speed =", SPEED
        elif action == 'backward':
            #bw.speed = SPEED
            #bw.counterclockwise()
            #bw_status = -1
            esc.backward()
        elif action == 'stop':
            esc.stop()
    # ============== Front wheels =============
        elif action == 'fwready':
            esc.set_speed(2)
            esc.center()
        elif action == 'fwleft':
            esc.left()
        elif action == 'fwright':
            esc.right()
        elif action == 'fwstraight':
            esc.center()
            
            
        elif 'fwturn' in action:
            print "turn %s" % action
        # ================ Camera =================
        elif action == 'camready':
            cam.ready()
            print "camready"
        elif action == "camleft":
            cam.turn_left(40)
            print "camleft"
        elif action == 'camright':
            cam.turn_right(40)
            print "camright"
        elif action == 'camup':
            cam.turn_up(20)
            print "camup"
        elif action == 'camdown':
            print "camdown"
            cam.turn_down(20)

    if 'speed' in request.GET:
        speed = int(request.GET['speed'])
        SPEED = speed
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
            SPEED = speed
        speed /= 12
        esc.set_speed(speed)
        
    host = stream.get_host().split(' ')[0]
    return render_to_response("run.html", {'host': host})

def connection_test(request):
	return HttpResponse('OK')
