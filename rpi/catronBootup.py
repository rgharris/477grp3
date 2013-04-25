#!/usr/bin/env python3

#This script writes a byte to a given i2c address and location.

import quick2wire.i2c as i2c
import sys,os
import random as r

MICROADDR = 0x50
PIREG = 0
STARTRAND = 10
BOOTUP = 1

def startBoard():
	r.seed() #Uses system time by default
	if os.path.isfile("/home/pi/477grp3/webapp/gameStatus.json"):
		os.remove("/home/pi/477grp3/webapp/gameStatus.json")
	with i2c.I2CMaster() as bus:
		while True:
			try:
				bus.transaction(i2c.writing_bytes(MICROADDR, STARTRAND, r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250))) #Too lazy to figure out the 'pythonic' way to do this. This should work. Repeated 19 times.
				bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, BOOTUP))
				break
			except:
				pass

if __name__ == "__main__":
	startBoard()
	print("Generated random board!")
