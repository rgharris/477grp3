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
	output = """<form method="post" action="index.py" class="trade">
     	      <h2 style="margin-bottom: 15px">Trade</h2>
	      <div style="width: 100%; height: 155px">
			<div class="resourceColumn">
				<h3 class="resourceHeader">Resource</h3>	
				<div class="resourceName">Clay</div>
				<div class="resourceName">Ore</div>
				<div class="resourceName">Sheep</div>
				<div class="resourceName">Wheat</div>
				<div class="resourceName">Wood</div>
			</div>
			<div class="countColumn">
				<h3 class="countHeader">Give</h3>
				<input name="giveClay" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="giveOre" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="giveSheep" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="giveWheat" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="giveWood" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
			</div>
			<div class="countColumn">
				<h3 class="countHeader">Get</h3>
				<input name="getClay" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="getOre" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="getSheep" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="getWheat" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
				<input name="getWood" type="number" class="countValue" value="0"  onfocus="{1}" onblur="{2}"/>
			</div>
			</div>
			<h3>Player to trade with: </h3>
			<select name="playerid" class="playerSelect">
				{0}
			</select>
				<input type="submit" value="No Deal!" class="bottom half left" name="noDeal" />
				<input type="submit" value="Deal!" class="bottom half right" name="deal" />
        	   </form>
			"""
	for fn in os.listdir(PLAYER_FILE):
		if fn != 'dev.json' and fn != 'trade.json':
			jsonInfo = open(PLAYER_FILE + fn)
			playerInfo = json.load(jsonInfo)
			playerID = os.path.splitext(os.path.basename(fn))[0] #I have no idea why I forced this hilarious stupidity upon myself.
			playerList.append("<option value=\"" + playerID + "\">" + playerInfo["playerName"] + "</option>")
			jsonInfo.close()
	output = output.format('\n'.join(playerList), "if(this.value == '0') { this.value = ''; }", "if(this.value == '') {this.value = '0';}")

else:
	if pairs.has_key("invalid"):
		if pairs['invalid'][0] == "current":
			#Shows up on currentplayer's screen to identify invalid.
			output = "<h2>Trade Error</h2>\n<p>You don't have enough resources to trade or you have selected an invalid option.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
		if pairs['invalid'][0] == "remote":
			jsonInfo = open(TRADE_FILE)
			tradeInfo = json.load(jsonInfo)
			output = "<form method=\"post\" action=\"index.py\">\n<h2>Trade Error</h2>\n<p>You don't have enough resources to trade.</p><input type=\"hidden\" value=\"" + str(tradeInfo['from']) + "\" name=\"tradeFrom\"><input type=\"submit\" value=\"Got it!\" class=\"bottom\" name=\"doNotTrade\"></form>"
	elif pairs.has_key("confirm"):
		#Shows up on remote player's screen to confirm trade.
		output = "<form method=\"post\" action=\"index.py\">\n<h2>Confirm Trade</h2>\n"
		jsonInfo = open(TRADE_FILE)
		tradeInfo = json.load(jsonInfo)
		getString = ''
		giveString = ''
		#Would really like to add some magic to throw "and" in there...
		if (len(tradeInfo['get']) == 1):
			for resource in tradeInfo['get']:
				 getString = getString + str(tradeInfo['get'][resource]) + " " + str(resource)
		else:
			for resource in tradeInfo['get']:
				 getString = getString + str(tradeInfo['get'][resource]) + " " + str(resource) + ", "
		if (len(tradeInfo['give']) == 1):
			for resource in tradeInfo['give']:
				 giveString = giveString + str(tradeInfo['give'][resource]) + " " + str(resource)
		else:
			for resource in tradeInfo['give']:
				 giveString = giveString + str(tradeInfo['give'][resource]) + " " + str(resource) + ", "
		output = output + "<p>Do you wish to trade " + getString + " for " + giveString + "?</p>"
		output = output + "<input type=\"hidden\" value=\"" + str(tradeInfo['from']) + "\" name=\"tradeFrom\"><input type=\"submit\" value=\"No I don't!\" class=\"bottom half left\" name=\"doNotTrade\"/><input type=\"submit\" value=\"Yes I do!\" class=\"bottom half right\" name=\"confirmTrade\"/></form>"
		jsonInfo.close()
	elif pairs.has_key("deny"):
		#Shows up on current player's screen to acknowledge denial of trade.
		output = "<h2>Trade denied</h2>\n<p>Your trade has been denied from the player you were trading with.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
	elif pairs.has_key("success"):
		#Shows up on current player's screen to acknowledge success of trade.
		output = "<h2>Trade Successful</h2>\n<p>Your trade has been accepted and has taken place.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"


print output
