#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the dialog that deals with trading.
# It should deal with both traders.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json

PLAYER_FILE = "../players/"
GAME_STATE_FILE = "../chkRefresh/gamestate.json"

query = os.environ["QUERY_STRING"]

pairs = cgi.parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")

if len(pairs) == 0:
	output = """<h2>Error!</h2>\n<p>This should never happen.</p>"""

else:
	read = pairs['read'][0]
	output = "<h2>Testing</h2>\n<p>confirm: " + str(pairs['confirm'][0]) + " and read: " + str(pairs['read'][0]) + "."
	if pairs['confirm'][0] == 1:
		if read % 10 == 0:
			piece = "thief"
		elif read % 10 == 1:
			piece = "road"
		elif read % 10 == 2:
			piece = "settlement"
		elif read % 10 == 3:
			piece = "city"
		output = "<form action=\"index.py\" method=\"post\"><h2>Confirm piece</h2>\n<p>Would you like to place a " + piece + " in the indicated location on the board?<input type=\"hidden\" value=\"" + piece + "\" name=\"pieceType\" /><input type=\"submit\" value=\"No I don't!\" class=\"bottom half left\" name=\"denyPiecePlacement\"/><input type=\"submit\" value=\"Yes I do!\" class=\"bottom half right\" name=\"confirmPiecePlacement\"/></form>"
	elif pairs['confirm'][0] == 2:
		if read < 30:
			action = "remove"
			if read % 20 == 0:
				piece = "thief"
			elif read % 20 == 1:
				piece = "road"
			elif read % 20 == 2:
				piece = "settlement"
			elif read % 20 == 3:
				piece = "city"
		else:
			action = "replace"
			if read % 30 == 0:
				piece = "thief"
			elif read % 30 == 1:
				piece = "road"
			elif read % 30 == 2:
				piece = "settlement"
			elif read % 30 == 3:
				piece = "city"
		output = "<h2>Error!</h2>\n<p>Please " + action + " the indicated " + piece + " on the board.</p>"
		
print(output)
