#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json



output = """Content-type: text/html;charset=utf-8

            <form method="post" action="index.py">
            <h2>Purchase</h2>
            <input type="submit" value="Settlement" class="bottom half top left" name="settle"/>
				<input type="submit" value="City" class="bottom half top right" name="city"/>
				<input type="submit" value="Road" class="bottom half bot left" name="road" />
				<input type="submit" value="Development Card" class="bottom half bot right" name="dev" />
            </form>
			"""

print output;
