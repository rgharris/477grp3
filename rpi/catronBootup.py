#!/usr/bin/env python3

#This script writes a byte to a given i2c address and location.

import quick2wire.i2c as i2c
import sys,os
import time #debugging...
import random as r

MICROADDR = 0x50
PIREG = 0
STARTRAND = 10
BOOTUP = 1
#Debugging...
STARTGAME = 2

if __name__ == "__main__":
	r.seed() #Uses system time by default
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, STARTRAND, r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250), r.randint(0,250))) #Too lazy to figure out the 'pythonic' way to do this. This should work. Repeated 19 times.
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, BOOTUP))
		time.sleep(1)
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, STARTGAME))
	print("Write attmpted. Completion not ensured.")
