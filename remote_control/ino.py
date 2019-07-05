import serial

class Ino:

	ser = serial.Serial('/dev/ttyACM0',9600)

	def sonic(self):
		data = 100
		try:
			data = self.ser.readline()
		except:
#			print "Arduino Except"
			pass

		return data

