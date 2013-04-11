#!/usr/bin/env python3

#This script writes a byte to a given i2c address and location.

import quick2wire.i2c as i2c
import sys,os

if __name__ == "__main__":
	if(len(sys.argv) != 4 or sys.argv[1] == "-h" or sys.argv[1] == "--help"):
		print("Usage: " + sys.argv[0] + " [i2c device address] [i2c location address] [byte to write]")
		print("Example: " + sys.argv[0] + " 0x50 0x13 0x20 would write 20 in register 13 of the i2c device at address 50.")
		print("This script only writes one byte at a time.")
	else:
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(int(sys.argv[1], 0), int(sys.argv[2], 0), int(sys.argv[3], 0)))
		print("Write attmpted. Completion not ensured.")
