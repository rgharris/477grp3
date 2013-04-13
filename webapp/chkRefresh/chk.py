#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is a really quick program that
# returns a 1 if they need to refresh,
# a 0 otherwise.
# It also checks for the I2C flag on the micro,
# and checks the approriate registers if it's set.
import os, cgi

query=os.environ[ "QUERY_STRING" ]

pairs = cgi.parse_qs(query)
pid = pairs['id'][0]

output = "Content-type: text/plain\n\n" + open(pid, 'r').read()

print(output);
