#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is a really quick program that
# returns a 1 if they need to refresh,
# a 0 otherwise.
# It also checks for the I2C flag on the micro,
# and checks the approriate registers if it's set.
import os, cgi
from quick2wire.gpio import pins, In, Out

query=os.environ[ "QUERY_STRING" ]

pairs = cgi.parse_qs(query)
pid = pairs['id'][0]
outVal = open(pid, 'r').read()
InPin = pins.pin(7, direction=In)
with InPin:
	if InPin.value == 1:
		outVal = 9 #i2c refresh value

output = "Content-type: text/plain\n\n" + str(outVal)

print(output);
