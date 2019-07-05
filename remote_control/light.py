import RPi.GPIO as GPIO
import time

class Light:

	left_pin = 4
	right_pin = 11	
	
	def __init__(self):
		#import RPi.GPIO as GPIO
		#import time
	
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.cleanup()
	
		#left_pin = 4
		#right_pin = 11
	
		GPIO.setup(self.left_pin, GPIO.OUT)
		GPIO.setup(self.right_pin, GPIO.OUT)

	def left(self):
		for i in range(0,10):
			GPIO.output(self.left_pin,True)
			time.sleep(0.1)
			GPIO.output(self.left_pin,False)
			time.sleep(0.1)

	def right(self):
		for i in range(0,10):
			GPIO.output(self.right_pin,True)
			time.sleep(0.1)
			GPIO.output(self.right_pin,False)
			time.sleep(0.1)

