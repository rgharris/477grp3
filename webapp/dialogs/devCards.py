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
PLAYER_FILE = "../players/"
pairs = cgi.parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")


if len(pairs) == 0:
	output = """<form method="post" action="index.py">
      	      <h2>Error!</h2>
		<p>This should never happen.</p>
				"""
else:
	playerFile = open(PLAYER_FILE + str(pairs["player"][0]) + ".json")
	playerInfo = json.load(playerFile)
	playerFile.close()

	if "confirm" in pairs:
		if pairs['confirm'][0] == "plenty":
			pass
		if pairs['confirm'][0] == "monopoly":
			pass
		if pairs['confirm'][0] == "road":
			pass
		if pairs['confirm'][0] == "knights":
			pass
		if pairs['confirm'][0] == "victory":
			pass

	elif "card" in pairs:
		if pairs['card'][0] == "plenty":
			if playerInfo['cards']['plenty'] > 0:
				output = """<form method="post" action="index.py">
						<h2>Year of Plenty Card</h2>
						<p>This card allows you to take two of any one resource you have a settlement on. You currently have {0} Year of Plenty cards available. Would you like to play one?</p>
					"""
			else:
				output = "<h2>Year of Plenty Card</h2>\n<p>This card allows you to take two of any one resource you have a settlement on. You currently have no Year of Plenty cards available.</p>"
		elif pairs['card'][0] == "monopoly":
			if playerInfo['cards']['monopoly'] > 0:
				output = """<form method="post" action="index.py">
						<h2>Monopoly Card</h2>
						<p>This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you. You currently have {1} Monopoly cards available. Would you like to play one?</p>
					"""
			else:
				output = "<h2>Monopoly card</h2>\n<p>This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you. You currently have no Monopoly cards available.</p>"
		elif pairs['card'][0] == "road":
			if playerInfo['cards']['road'] > 0:
				output = """<form method="post" action="index.py">
						<h2>Road Building Card</h2>
						<p>This card allows you to place two roads at no additional cost. You currently have {2} Road Building cards available. Would you like to play one?</p>
					"""
			else:
				output = "<h2>Road Building Card</h2>\n<p>This card allows you to place two roads at no additional cost. You have no road building cards available.</p>"
		elif pairs['card'][0] == "knights":
			if playerInfo['cards']['knights'] > 0:
				output = """<form method="post" action="index.py">	
						<h2>Knight card</h2>
						<p>This card allows you to move the thief and steal a single, random resource from a given player. You have played {5} knight cards, and currently have {3} unplayed Knight cards available. Would you like to play one?</p>
					"""
			else:
				output = "<h2>Knight card</h2>\n<p>This card allows you to move the thief and steal a single, random resource from a given player. You have played {5} knight cards, and have none available.</p>"
		elif pairs['card'][0] == "victory":
			output = """<h2>Victory card</h2>
					<p>This card gets you an additional victory point, hidden from the other players. It cannot be played, but counts toward your total score. Your opponents will only see your score without these cards. You currently have {4} victory cards.</p>
				"""
	else:
		output = """<form method="post" action="index.py" class="cards">
				<h2>Development Cards</h2>
				<p>You have the following available.</p>
				<input type="submit" value="Victory: {4}" class="bottom moreTop left" name="victory" />
				<input type="submit" value="Monopoly: {1}" class="bottom half top left" name="monopoly" />
				<input type="submit" value="Road Building: {2}" class="bottom half top right" name="road" />
				<input type="submit" value="Knight: {3}" class="bottom half bot left" name="knights" />
				<input type="submit" value="Year of Plenty: {0}" class="bottom half bot right" name="plenty" />
			    </form>"""


output = output.format(playerInfo['cards']['plenty'], playerInfo['cards']['monopoly'], playerInfo['cards']['road'], playerInfo['cards']['knights'], playerInfo['cards']['victory'] + playerInfo['onHold']['victory'], playerInfo['playedKnights'])
print(output)
