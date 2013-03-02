#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi

query=os.environ[ "QUERY_STRING" ]

pairs = cgi.parse_qs(query)

output = """Content-type: text/html;charset=utf-8

            <form method="post" action="index.py">
            <h2>Please enter your username.</h2>
            <div>
               <input type="text" id="user" name="user" value="{0}" />
            </div>
            <input type="submit" value="Got it!" class="bottom" />
            </form>
			"""

print output.format(pairs['user']);
