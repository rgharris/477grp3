#!/usr/bin/env python3
#
#This file is a quick and easy CLI for communicating with
#the microcontroller over i2c.
#
#Parameters: address of the i2c slave.
import time, os, sys, select
import quick2wire.i2c as i2c
from quick2wire.gpio import Pin, In, Out, Both
from quick2wire.selector import Selector

#The pin used to throw an I2C interrupt
GPIOPIN = 4
#Register that tells us how many bytes to read
#when we're reading from I2C. Should only be
#one byte long.
NBYTEREGISTER = 0xFE
#The register and value we need to write
#to in order to tell the micro that we've
#successfully read the information.
CLEARREGISTER = 0xFF
CLEARVALUE = 0x00
#This register is the starting register to read from
STARTREGISTER = 0x00

def i2cReadData(address):
	print("Receiving data...")
	with i2c.I2CMaster() as bus:
		#First, read to see how many bytes to read. Yeah, I know...
		read_num = bus.transaction(i2c.writing_bytes(address, NBYTEREGISTER), i2c.reading(address, 1))
		#Now we read that many bytes, starting at the first register
		read_result = bus.transaction(i2c.writing_bytes(address, STARTREGISTER), i2c.reading(address, read_num))
	print(read_result)

def i2cWriteData(address):
	print("Type q to quit writing.")
	tosend = input('To Microcontroller (format is register:bytes):')
	while (tosend != "q"):
		register,bytes = tosend.split(':',1)
		#Setup I2C Master object to set RPI as master
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing(address,register + bytes))
		print("Complete.")
		print()
		print("Press any key to send command, CTRL+C to exit.")
	
def runTerminal(address):
	#Setup terminal
	print("Press any key to send command, CTRL+C to exit.")
	#dataFlag = Pin(GPIOPIN, direction=In, interrupt="rising")
	dataFlag = pins.pin(GPIOPIN, In, pins.Rising)
	#Setup epoll, sort of like C's select statement
	epoll = select.epoll()
	#Register the pin, wait for level changes
	epoll.register(dataFlag, select.EPOLLIN | select.EPOLLET)
	#Register standard input (the keyboard), wait for input
	#Since we're going to do something on keypress, we won't be able
	#to grab events from the micro while typing. This is fine, because
	#it won't be an issue in the interface - reading and writing will be
	#independant.
	#
	#Should we just have a function in the "ttl" file (which doesn't exist yet)
	#that's called on the web interface that checks the GPIO level? If so,
	#that would make things easier (no need to write a daemon for this), but
	#it would mean there's up to 5 seconds (or whatever the ttl refresh value is)
	#where the pi could not react to the micro.
	#Something to think about.
	epoll.register(sys.stdin, select.EPOLLIN)
	#Endless loop waiting for something.
	while True:
		events = epoll.poll()
		for fileno, event in events:
			if fileno == sys.stdin.fileno():
				i2cWriteData(address)
			if fileno == pin.fileno():
				i2cReadData(address)

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print("Usage: " + sys.argv[0] + " address")
		print("Address should be in 0xYY format, with YY being the hex address.")
	else:
		runTerminal(sys.argv[1])
