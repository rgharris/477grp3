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
TRADE_FILE = "../players/trade.json"

query = os.environ["QUERY_STRING"]

pairs = cgi.parse_qs(query)
playerList = []

print "Content-type: text/html;charset=utf-8\n\n"

if len(pairs) == 0:
	#Shows on current player's screen to run trade.
	output = """<form method="post" action="index.py">
     	      <h2>Trade</h2>
				Give:
				<input type="number" class="modalNumber" name="giveNumber" min="1" max="99"/> &nbsp; <select name="tradeGive" class="modalSelect">
					<option value="none">Select Resource</option>
					<option value="clay">Clay</option>
					<option value="ore">Ore</option>
					<option value="wheat">Wheat</option>
					<option value="sheep">Sheep</option>
					<option value="wood">Wood</option></select><br />
				Get:
				<input type="number" class="modalNumber" name="getNumber" min="1" max="99"/> &nbsp; <select name="tradeGet" class="modalSelect">
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
		if pairs['invalid'][0] == "current":
			#Shows up on currentplayer's screen to identify invalid.
			output = "<h2>Trade Error</h2>\n<p>You don't have enough resources to trade or you have selected an invalid option.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
		if pairs['invalid'][0] == "remote":
			output = "<form method=\"post\" action=\"index.py\">\n<h2>Trade Error</h2>\n<p>You don't have enough resources to trade.</p><input type=\"submit\" value=\"Got it!\" class=\"bottom\" name=\"doNotTrade\"></form>"
	elif pairs.has_key("valid"):
		#Shows up on current player's screen to ask for player to trade with.
		output = """<form method="post" action="index.py">
				<h2>Trade</h2>
				With:
				<select name='playerid' class="modalSelect"> {0}
				</select>
				<input type="submit" value="Nevermind." class="bottom half left" name="noDeal" />
				<input type="submit" value="Let's do it!" class="bottom half right" name="performTrade" />
				</form>
			"""
		for fn in os.listdir(PLAYER_FILE):
			if fn != 'dev.json' and fn != 'trade.json':
				jsonInfo = open(PLAYER_FILE + fn)
				playerInfo = json.load(jsonInfo)
				playerID = os.path.splitext(os.path.basename(fn))[0] #I have no idea why I forced this hilarious stupidity upon myself.
				playerList.append("<option value=\"" + playerID + "\">" + playerInfo["playerName"] + "</option>")
				jsonInfo.close()
		output = output.format('\n'.join(playerList))
	elif pairs.has_key("confirm"):
		#Shows up on remote player's screen to confirm trade.
		output = "<form method=\"post\" action=\"index.py\">\n<h2>Confirm Trade</h2>\n"
		jsonInfo = open(TRADE_FILE)
		tradeInfo = json.load(jsonInfo)
		output = output + "<p>Do you wish to trade " + str(tradeInfo['get']['amount']) + " " + tradeInfo['get']['resource'] + " for " + str(tradeInfo['give']['amount']) + " " + tradeInfo['give']['resource'] + "?</p>"
		output = output + "<input type=\"hidden\" value=\"" + str(tradeInfo['from']) + "\" name=\"tradeFrom\"><input type=\"submit\" value=\"No I don't!\" class=\"bottom half left\" name=\"doNotTrade\"/><input type=\"submit\" value=\"Yes I do!\" class=\"bottom half right\" name=\"confirmTrade\"/></form>"
		jsonInfo.close()
	elif pairs.has_key("deny"):
		#Shows up on current player's screen to acknowledge denial of trade.
		output = "<h2>Trade denied</h2>\n<p>Your trade has been denied from the player you were trading with.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
	elif pairs.has_key("success"):
		#Shows up on current player's screen to acknowledge success of trade.
		output = "<h2>Trade Successful</h2>\n<p>Your trade has been accepted and has taken place.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"


print output
