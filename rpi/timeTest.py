#!/usr/bin/python3

import quick2wire.i2c as i2c
from quick2wire.gpio import pins,In,Out
import time

times = []
start = time.time()
inPin = pins.pin(7, direction=In)
with inPin:
	if inPin.value == 1:
		pass
	else:
		pass
times.append(time.time() - start)
start = time.time()
with i2c.I2CMaster() as bus:
	readMCU = bus.transaction(i2c.writing_bytes(0x50, 3), i2c.reading(0x50, 1))
times.append(time.time() - start)
print(times)
