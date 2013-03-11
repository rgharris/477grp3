#!/usr/bin/env python
#
#This file is a quick and easy CLI for communicating with
#the microcontroller over i2c.
#
#Parameters: address of the i2c slave.
import time, os, sys

#Use Adafruit's rPI library for GPIO,
#as it has better interrupt handling.
import rPI.GPIO as gpio

#Use quick2wire's I2C libraries,
#as they seem easier to use and more
#robust.
import quick2wire.i2c as i2c

bus = smbus.SMBus(1)

def i2cReceiveData():

def runTerminal(address):
	#Setup GPIO
	gpio.setmode(gpio.BOARD)
	gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

	#Start loop as I2C Master. Loops infinitely.
	with i2c.I2CMaster() as bus:
		gpio.add_event_detect(4,gpio.RISING, i2cReceiveData)
	
if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print "Usage: " + sys.argv[0] + " address"
		print "Address should be in 0xYY format, with YY being the hex address."
	else:
		runTerminal(sys.argv[1])
