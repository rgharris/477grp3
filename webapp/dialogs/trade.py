#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the dialog that deals with trading.
# It should deal with both traders.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json

PLAYER_FILE = "../players/"

query = os.environ["QUERY_STRING"]

pairs = cgi.parse_qs(query)

print "Content-type: text/html;charset=utf-8\n\n"

if len(pairs) == 0:
	playerList = []
	#Shows on current player's screen to run trade.
	output = """<form method="post" action="index.py">
     	      <h2>Trade</h2>
				Give:
				<input type="number" class="modalNumber" name="tradeNumber" min="1" max="99"/> &nbsp; <select class="modalSelect">
					<option value="none">Select Resource</option>
					<option value="clay">Clay</option>
					<option value="ore">Ore</option>
					<option value="wheat">Wheat</option>
					<option value="sheep">Sheep</option>
					<option value="wood">Wood</option></select><br />
				Get:
				<input type="number" class="modalNumber" name="forNumber" min="1" max="99"/> &nbsp; <select class="modalSelect">
					<option value="none">Select Resource</option>
					<option value="clay">Clay</option>
					<option value="ore">Ore</option>
					<option value="wheat">Wheat</option>
					<option value="sheep">Sheep</option>
					<option value="wood">Wood</option></select>
				<input type="submit" value="No Deal!" class="bottom half left" name="noDeal" />
				<input type="submit" value="Deal!" class="bottom half right" name="deal" />
        	   </form>
			"""
else:
	if pairs.has_key("invalid"):
		#Shows up on current /or/ remote player's screen to identify invalid.
		output = "<h2>Trade Error</h2>\n<p>You don't have enough resources to trade with " + pairs["invalid"][0] + "</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
	elif pairs.has_key("valid"):
		#Shows up on current player's screen to ask for player to trade with.
		output = """<form method="post" action="index.py">
				<h2>Trade</h2>
				From:
				<select class="modalSelect"> {0}
				</select>
				<input type="submit" value="Nevermind." class="bottom half left" name="noDeal" />
				<input type="submit" value="Let's do it!" class="bottom half right" name="trade" />
				</form>
			"""
		for fn in os.listdir(PLAYER_FILE):
			if fn != 'dev.json':
				jsonInfo = open(PLAYER_FILE + fn)
				playerInfo = json.load(jsonInfo)
				playerList.append("<option value=\"" + playerInfo["playerName"] + "\">" + playerInfo["playerName"] + "</option>")
				jsonInfo.close()
		output = output.format('\n'.join(playerList))
	elif pairs.has_key("confirm"):
		#Shows up on remote player's screen to confirm trade.
		output = "<form method=\"post\" action=\"index.py\">\n<h2>Confirm Trade</h2>\n"
		#Remember, all variables are from the perspective of the current player's turn, so this looks backwards but it is not.
		output = output + "<p>Do you wish to trade " + pairs["forNum"] + " " + pairs["for"] + " for " + pairs["getNum"] + " " + pairs["get"] + "?</p>"
		output = output + "<input type=\"submit\" value=\"Yes I do!\" class=\"bottom half left\" name=\"confirmPurchase\"/><input type=\"submit\" value=\"No I don't!\" class=\"bottom half right\" name=\"doNotPurchase\"/>"
	elif pairs.has_key("deny"):
		#Shows up on current player's screen to acknowledge denial of trade.
		output = "<h2>Trade denied</h2>\n<p>Your trade has been denied from the player you were trading with.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"


print output
