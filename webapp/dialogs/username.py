#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.

from os import environ
from cgi import parse_qs

query=environ[ "QUERY_STRING" ]

pairs = parse_qs(query)

output = """Content-type: text/html;charset=utf-8

            <form method="post" action="index.py">
            <h2>Please enter your username.</h2>
            <div>
               <input type="text" id="user" name="user" value="{0}" />
            </div>
            <input type="submit" value="Got it!" class="bottom left" />
            </form>
			"""

print(output.format(pairs['user'][0]));
