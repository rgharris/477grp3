#!/usr/bin/env python
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

print "Content-type: text/html;charset=utf-8\n\n"

if len(pairs) == 0:
	output = """<form method="post" action="index.py">
      	      <h2>Purchase</h2>
         	   <input type="submit" value="Settlement" class="bottom half top left" name="settle"/>
					<input type="submit" value="City" class="bottom half top right" name="city"/>
					<input type="submit" value="Road" class="bottom half bot left" name="road" />
					<input type="submit" value="Dev. Card" class="bottom half bot right" name="dev" />
	        	   </form>
				"""
else:
	if pairs.has_key("invalid"):
		humanMap = {"settle":"settlement", "city":"city", "road":"road", "dev":"development card"}
		output = "<h2>Purchase Error</h2>\n<p>You don't have enough resources to purchase a " + humanMap[pairs["invalid"][0]] + "!</p><a href=\"index.py#x\" class=\"bottom\">Got it!</a>"
	elif pairs.has_key("confirm"):
		output = "<form method=\"post\" action=\"index.py\">\n<h2>Confirm Purchase</h2>\n"
		if pairs["confirm"][0] == "settle":
			output.append("<p>Do you wish to purchase a settlement for 1 wood, 1 wheat, 1 sheep, and 1 clay?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"settle\" />")
		elif pairs["confirm"][0] == "city":
			output.append("<p>Do you wish to purchase a city for 2 wheat and 3 ore?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"city\" />")
		elif pairs["confirm"][0] == "road":
			output.append("<p>Do you wish to purchase a road for 1 wood and 1 clay?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"road\" />")
		elif pairs["confirm"][0] == "dev":
			output.append("<p>Do you wish to purchase a development card for 1 wheat, 1 sheep, and 1 ore?</p>\n<input type=\"hidden\" name=\"purchase\" value=\"dev\" />")
		output.append("<input type=\"submit\" value=\"Yes I do!\" class=\"bottom half left\" name=\"purchase\"/><input type=\"submit\" value=\"No I don't!\" class=\"bottom half right\" name=\"doNotPurchase\"/>")
	elif pairs.has_key("place"):
		output = "<h2>Place piece</h2>\n<p>Please place your piece now.</p><a href=\"index.py#x\" class=\"bottom\">Done.</a>"


print output
