#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json

PLAYER_FILE="../players/"

print "Content-type: text/html;charset=utf-8"
print
print "<h2>Game Status</h2>\n"
print "\t<ul class=\"gameStatus\">\n"
for fn in os.listdir(PLAYER_FILE):
	if fn != 'dev.json' and fn != 'trade.json':
		jsonInfo = open(PLAYER_FILE + fn)
		playerInfo = json.load(jsonInfo)
		print "\t\t<li><b>" + playerInfo["playerName"] + "</b> &nbsp; &nbsp; " + str(playerInfo["points"]) + " points"
		if len(playerInfo["awards"]) > 0:
			if len(playerInfo["awards"]) == 1 and playerInfo["awards"][0] == "road":
				print "<br />\n\t\t<i>Has the longest road</i>"
			elif len(playerInfo["awards"]) == 1 and playerInfo["awards"][0] == "army":
				print "<br />\n\t\t<i>Has the largest army</i>"
			elif len(playerInfo["awards"]) == 2:
				print "<br />\n\t\t<i>Has the longest road and the largest army</i>"
		print "</li>\n"
		jsonInfo.close()
print"</ul>\t<a href=\"#x\" class=\"bottom\">Got it!</a>"
