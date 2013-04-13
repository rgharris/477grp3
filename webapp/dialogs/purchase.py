#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json

query = os.environ["QUERY_STRING"]

pairs = cgi.parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")

if len(pairs) == 0:
	output = """<form method="post" action="index.py">
      	      <h2>Purchase</h2>
         	   <input type="submit" value="Settlement" class="bottom half top left" name="settle"/>
					<input type="submit" value="City" class="bottom half top right" name="city"/>
					<input type="submit" value="Road" class="bottom half bot left" name="road" />
					<input type="submit" value="Dev. Card" class="bottom half bottom right" name="dev" />
	        	   </form>
				"""
else:
	if "invalid" in pairs:
		humanMap = {"settle":"settlement", "city":"city", "road":"road", "dev":"development card"}
		output = "<h2>Purchase Error</h2>\n<p>You don't have enough resources to purchase a " + humanMap[pairs["invalid"][0]] + "!</p><a href=\"index.py#x\" class=\"bottom left\">Got it!</a>"
	elif "confirm" in pairs:
		output = "<form method=\"post\" action=\"index.py\">\n<h2>Confirm Purchase</h2>\n"
		if pairs["confirm"][0] == "settle":
			output = output + "<p>Do you wish to purchase a settlement for 1 wood, 1 wheat, 1 sheep, and 1 clay?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"settle\" />"
		elif pairs["confirm"][0] == "city":
			output = output + "<p>Do you wish to purchase a city for 2 wheat and 3 ore?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"city\" />"
		elif pairs["confirm"][0] == "road":
			output = output + "<p>Do you wish to purchase a road for 1 wood and 1 clay?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"road\" />"
		elif pairs["confirm"][0] == "dev":
			output = output + "<p>Do you wish to purchase a development card for 1 wheat, 1 sheep, and 1 ore?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"dev\" />"
		output = output + "<input type=\"submit\" value=\"Yes I do!\" class=\"bottom half left\" name=\"confirmPurchase\"/><input type=\"submit\" value=\"No I don't!\" class=\"bottom half right\" name=\"doNotPurchase\"/>"
	elif "place" in pairs:
		output = "<h2>Place piece</h2>\n<p>Please place your piece now.</p><!--TODO:This needs removed when we're communicating with the board.--><a href=\"index.py#x\" class=\"bottom\">Done.</a>"
	elif "obtained" in pairs:
		humanMap = {"knights":"Knight", "monopoly":"Monopoly", "road":"Road Building", "plenty":"Year of Plenty", "victory":"Victory Point"}
		if pairs["obtained"][0] != "victory":
			output = "<h2>Development Card!</h2>\n<p>You have received a " + humanMap[pairs["obtained"][0]] + " card! You can play it any time, starting next turn, by selecting the \"Dev Cards\" item on the resource screen.</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
		else:
			output = "<h2>Victory Card!</h2>\n<p>Congratulations! You are one step closer to victory! You have obtained a victory point card. No one will see this victory point until the end of the game, and it will not show up in the status screen. It will only show up on your main point count next to your name.</p><a href=\"index.py#x\" class=\"bottom\">Awesome!</a>"
	elif "development" in pairs:
		if pairs["development"][0] == "none":
			output = "<h2>No development cards!</h2>\n<p>There are no development cards to draw! Pick another thing to purchase, if you are able.</p><a href=\"index.py#x\" class=\"bottom\">Got it.</a>"


print(output)
