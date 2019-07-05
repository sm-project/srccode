#!/usr/bin/env python
__author__ = 'skunda'
# This program logs a Raspberry Pi's CPU temperature to a Thingspeak Channel
# To use, get a Thingspeak.com account, set up a channel, and capture the Channel Key at https://thingspeak.com/docs/tutorials/ 
# Then paste your channel ID in the code for the value of "key" below.
# Then run as sudo python pitemp.py (access to the CPU temp requires sudo access)
# You can see my channel at https://thingspeak.com/channels/41518

import httplib, urllib
import time
import smbus
bus = smbus.SMBus(1)
global dat
dat = 0x48
sleep = 0 # how many seconds to sleep between posts to the channel
key = 'NKP3ZABMT8W2YD8O'  # Thingspeak channel to update
global flag
flag = False
#Report Raspberry Pi internal temperature to Thingspeak Channel
def thermometer():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
#        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
	bus.write_byte(dat,0x70)
	temp = bus.read_byte(dat)
	bus.write_byte(dat,0x48)
	regi = bus.read_byte(dat)       
	params = urllib.urlencode({'field1': temp, 'field2': regi, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print "Send"
   #         print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        if not flag:
		break
#	time.sleep(5)

#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                thermometer()
 #               time.sleep(sleep)
#
