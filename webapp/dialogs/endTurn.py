#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi

output = """Content-type: text/html;charset=utf-8

            <form method="post" action="index.py">
            <h2>End Turn</h2>
				<p>Are you sure you want to end your turn?</p>
            <input type="submit" value="Yes I do!" class="bottom half left" name="endTurn"/>
				<input type="submit" value="Not yet!" class="bottom half right" name="noEndTurn"/>
            </form>
			"""

print output;
